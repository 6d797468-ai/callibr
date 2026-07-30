from __future__ import annotations

import pytest
from callibr_contracts import (
    ProcedureDefinition,
    ScenarioDefinition,
    ScenarioMetadata,
    ScenarioObjective,
    ScenarioReference,
    StepDefinition,
)
from callibr_kernel import CallibrError, EventBus
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_scenario.composer import ScenarioRegistry, ScenarioService, ScenarioValidator


class _InMemoryAuditStore:
    def __init__(self) -> None:
        self.records: list[object] = []

    def append(self, record: object) -> None:
        self.records.append(record)

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[object]:
        return [
            r
            for r in self.records
            if r.aggregate_type == aggregate_type and r.aggregate_id == aggregate_id
        ]


class _InMemoryScenarioDefStore:
    def __init__(self) -> None:
        self._data: dict[str, ScenarioDefinition] = {}

    def save(self, definition: ScenarioDefinition) -> None:
        self._data[definition.scenario_id] = definition

    def get(self, scenario_id: str) -> ScenarioDefinition | None:
        return self._data.get(scenario_id)

    def list(self) -> list[ScenarioDefinition]:
        return list(self._data.values())


class _InMemoryProcedureStore:
    def __init__(self) -> None:
        self._definitions: dict[str, ProcedureDefinition] = {}

    def save_definition(self, definition: ProcedureDefinition) -> None:
        self._definitions[definition.procedure_id] = definition

    def get_definition(self, procedure_id: str) -> ProcedureDefinition | None:
        return self._definitions.get(procedure_id)

    def list_definitions(self) -> list[ProcedureDefinition]:
        return list(self._definitions.values())

    def save_execution(self, execution: object) -> None:
        pass

    def get_execution(self, execution_id: str) -> object | None:
        return None

    def list_executions(self, procedure_id: str) -> list[object]:
        return []


SAMPLE_SCENARIO = ScenarioDefinition(
    scenario_id="sales-discovery",
    version="1.0.0",
    name="Sales Discovery",
    reference=ScenarioReference(
        procedure_id="qualification-commerciale",
        persona_id="sales-manager",
        crm_context_key="smb",
        rule_ids=["objection-handling", "qualification"],
    ),
    objectives=[
        ScenarioObjective(
            objective_id="discover_need",
            label="Discover customer need",
        ),
        ScenarioObjective(
            objective_id="identify_budget",
            label="Identify budget",
        ),
    ],
    metadata=ScenarioMetadata(
        difficulty="intermediate",
        estimated_minutes=15,
        tags=["sales", "discovery"],
    ),
)

SAMPLE_PROCEDURE = ProcedureDefinition(
    procedure_id="qualification-commerciale",
    name="Qualification Commerciale",
    version="1.0.0",
    steps=[
        StepDefinition(step_id="greeting", type="greeting", title="Accueil", next_step="discovery"),
        StepDefinition(
            step_id="discovery", type="discovery", title="Discovery", next_step="closing"
        ),
        StepDefinition(step_id="closing", type="closing", title="Closing"),
    ],
)


def _make_service() -> tuple[ScenarioService, _InMemoryAuditStore]:
    scenario_registry = ScenarioRegistry()
    proc_registry = ProcedureRegistry()
    proc_registry.register(SAMPLE_PROCEDURE)
    proc_store = _InMemoryProcedureStore()
    proc_store.save_definition(SAMPLE_PROCEDURE)
    validator = ScenarioValidator(
        procedure_registry=proc_registry,
        procedure_store=proc_store,
    )
    scenario_store = _InMemoryScenarioDefStore()
    audit = _InMemoryAuditStore()
    event_bus = EventBus()

    proc_executor = ProcedureExecutor()
    proc_service = ProcedureService(
        registry=proc_registry,
        executor=proc_executor,
        store=proc_store,
        audit_event_store=audit,
        event_bus=event_bus,
    )

    service = ScenarioService(
        registry=scenario_registry,
        validator=validator,
        store=scenario_store,
        procedure_service=proc_service,
        audit_event_store=audit,
        event_bus=event_bus,
    )
    return service, audit


# ---------- Definition ----------


def test_define_valid_scenario() -> None:
    service, _ = _make_service()
    result = service.define(SAMPLE_SCENARIO)
    assert result.scenario_id == "sales-discovery"
    assert result.reference.procedure_id == "qualification-commerciale"


def test_define_invalid_scenario_missing_id() -> None:
    service, _ = _make_service()
    invalid = ScenarioDefinition(
        scenario_id="",
        name="Bad",
        reference=ScenarioReference(procedure_id="x", persona_id="y"),
    )
    with pytest.raises(CallibrError) as exc:
        service.define(invalid)
    assert "INVALID_SCENARIO" in exc.value.code


def test_define_invalid_scenario_missing_procedure() -> None:
    service, _ = _make_service()
    invalid = ScenarioDefinition(
        scenario_id="test",
        name="Test",
        reference=ScenarioReference(procedure_id="nonexistent", persona_id="y"),
    )
    with pytest.raises(CallibrError) as exc:
        service.define(invalid)
    assert "INVALID_SCENARIO" in exc.value.code


def test_get_scenario() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    result = service.get("sales-discovery")
    assert result.name == "Sales Discovery"


def test_get_missing_scenario_raises() -> None:
    service, _ = _make_service()
    with pytest.raises(CallibrError) as exc:
        service.get("nonexistent")
    assert "SCENARIO_NOT_FOUND" in exc.value.code


def test_list_scenarios() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    results = service.list()
    assert len(results) == 1
    assert results[0].scenario_id == "sales-discovery"


# ---------- Validate ----------


def test_validate_valid_scenario() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    result = service.validate("sales-discovery")
    assert result.valid is True
    assert len(result.errors) == 0


def test_validate_scenario_with_warnings() -> None:
    service, _ = _make_service()
    no_objectives = ScenarioDefinition(
        scenario_id="no-obj",
        name="No Objectives",
        reference=ScenarioReference(procedure_id="qualification-commerciale", persona_id="x"),
        objectives=[],
    )
    service.define(no_objectives)
    result = service.validate("no-obj")
    assert result.valid is True
    assert len(result.warnings) >= 1


# ---------- Compose ----------


def test_compose_plan() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan = service.compose("sales-discovery", tenant_id="tenant_demo", actor_id="agent_001")
    assert plan.plan_id.startswith("plan_")
    assert plan.scenario.scenario_id == "sales-discovery"
    assert plan.execution_context["actor_id"] == "agent_001"
    assert plan.execution_context["procedure_id"] == "qualification-commerciale"
    assert plan.execution_context["persona_id"] == "sales-manager"
    assert len(plan.execution_context["objectives"]) == 2


def test_compose_with_extra_context() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan = service.compose(
        "sales-discovery",
        extra_context={"channel": "chat", "language": "fr"},
    )
    assert plan.execution_context["channel"] == "chat"
    assert plan.execution_context["language"] == "fr"


# ---------- Launch ----------


def test_launch_execution() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan = service.compose("sales-discovery", tenant_id="tenant_demo", actor_id="agent_001")
    result = service.launch(plan)
    assert result.execution_id is not None
    assert result.execution_id.startswith("proc-exec_")
    assert result.status == "running"
    assert result.procedure_id == "qualification-commerciale"
    assert len(audit.records) >= 1


def test_launch_produces_audit_event() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan = service.compose("sales-discovery")
    service.launch(plan)
    event_types = [r.event_type for r in audit.records]
    assert "scenario.launched" in event_types


# ---------- Multi-tenant isolation ----------


def test_scenario_tenant_context_in_plan() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan = service.compose("sales-discovery", tenant_id="tenant_acme", actor_id="agent_acme")
    assert plan.tenant_id == "tenant_acme"
    assert plan.actor_id == "agent_acme"


def test_scenario_isolation_between_tenants() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_SCENARIO)
    plan_a = service.compose("sales-discovery", tenant_id="tenant_a")
    plan_b = service.compose("sales-discovery", tenant_id="tenant_b")
    assert plan_a.plan_id != plan_b.plan_id
    assert plan_a.tenant_id != plan_b.tenant_id
