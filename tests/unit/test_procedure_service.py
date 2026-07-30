from __future__ import annotations

import pytest
from callibr_contracts import (
    AdvanceProcedureRequest,
    ProcedureDefinition,
    StartProcedureRequest,
    StepDefinition,
)
from callibr_kernel import CallibrError, EventBus
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry


class _InMemoryProcedureStore:
    def __init__(self) -> None:
        self._definitions: dict[str, ProcedureDefinition] = {}
        self._executions: dict[str, object] = {}

    def save_definition(self, definition: ProcedureDefinition) -> None:
        self._definitions[definition.procedure_id] = definition

    def get_definition(self, procedure_id: str) -> ProcedureDefinition | None:
        return self._definitions.get(procedure_id)

    def list_definitions(self) -> list[ProcedureDefinition]:
        return list(self._definitions.values())

    def save_execution(self, execution: object) -> None:
        self._executions[execution.execution_id] = execution  # type: ignore[union-attr]

    def get_execution(self, execution_id: str) -> object | None:
        return self._executions.get(execution_id)

    def list_executions(self, procedure_id: str) -> list[object]:
        return [e for e in self._executions.values() if e.procedure_id == procedure_id]  # type: ignore[union-attr]


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


SAMPLE_STEPS = [
    StepDefinition(
        step_id="greeting",
        type="greeting",
        title="Accueil client",
        next_step="discovery",
    ),
    StepDefinition(
        step_id="discovery",
        type="discovery",
        title="Decouverte du besoin",
        next_step="closing",
    ),
    StepDefinition(step_id="closing", type="closing", title="Cloture"),
]

SAMPLE_PROCEDURE = ProcedureDefinition(
    procedure_id="qualification-commerciale",
    name="Qualification Commerciale",
    version="1.0.0",
    description="Procedure de qualification d'un prospect",
    steps=SAMPLE_STEPS,
)


def _make_service() -> tuple[ProcedureService, _InMemoryAuditStore]:
    registry = ProcedureRegistry()
    executor = ProcedureExecutor()
    store = _InMemoryProcedureStore()
    audit = _InMemoryAuditStore()
    event_bus = EventBus()
    service = ProcedureService(registry, executor, store, audit, event_bus)
    return service, audit


# ---------- Definition ----------


def test_define_valid_procedure() -> None:
    service, _ = _make_service()
    result = service.define(SAMPLE_PROCEDURE)
    assert result.procedure_id == "qualification-commerciale"
    assert len(result.steps) == 3


def test_define_invalid_procedure_raises() -> None:
    service, _ = _make_service()
    invalid = ProcedureDefinition(
        procedure_id="",
        name="",
        description="",
        steps=[],
    )
    with pytest.raises(CallibrError) as exc:
        service.define(invalid)
    assert "INVALID_PROCEDURE" in exc.value.code


def test_get_procedure() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    result = service.get_procedure("qualification-commerciale")
    assert result.name == "Qualification Commerciale"


def test_get_missing_procedure_raises() -> None:
    service, _ = _make_service()
    with pytest.raises(CallibrError) as exc:
        service.get_procedure("nonexistent")
    assert "PROCEDURE_NOT_FOUND" in exc.value.code


def test_list_procedures() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    summaries = service.list_procedures()
    assert len(summaries) == 1
    assert summaries[0].procedure_id == "qualification-commerciale"
    assert summaries[0].step_count == 3


# ---------- Execution ----------


def test_start_execution() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(
        StartProcedureRequest(
            procedure_id="qualification-commerciale",
            tenant_id="tenant_demo",
            actor_id="agent_001",
            initial_context={"customer_name": "Amal"},
        )
    )
    assert execution.status == "running"
    assert execution.current_step_id == "greeting"
    assert execution.context["actor_id"] == "agent_001"
    assert execution.context["customer_name"] == "Amal"
    assert len(audit.records) == 1


def test_start_missing_procedure_raises() -> None:
    service, _ = _make_service()
    with pytest.raises(CallibrError) as exc:
        service.start(StartProcedureRequest(procedure_id="nonexistent"))
    assert "PROCEDURE_NOT_FOUND" in exc.value.code


def test_advance_to_next_step() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    updated = service.advance(
        execution.execution_id,
        AdvanceProcedureRequest(step_id="greeting", output={"result": "ok"}),
    )
    assert updated.current_step_id == "discovery"
    assert len(updated.completed_step_ids) == 1
    assert "greeting" in updated.completed_step_ids
    assert len(audit.records) == 2


def test_advance_completes_procedure() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    service.advance(
        execution.execution_id,
        AdvanceProcedureRequest(step_id="greeting"),
    )
    service.advance(
        execution.execution_id,
        AdvanceProcedureRequest(step_id="discovery", output={"score": 85}),
    )
    updated = service.advance(
        execution.execution_id,
        AdvanceProcedureRequest(step_id="closing"),
    )
    assert updated.status == "completed"
    assert updated.current_step_id is None
    assert len(updated.completed_step_ids) == 3


def test_fail_step() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    updated = service.fail(execution.execution_id, "greeting", "Customer unreachable")
    assert updated.status == "failed"
    assert updated.steps[0].error == "Customer unreachable"
    assert len(audit.records) == 2


def test_complete_execution_with_score() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    updated = service.complete(execution.execution_id, score=92)
    assert updated.status == "completed"
    assert updated.score == 92


def test_abort_execution() -> None:
    service, audit = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    updated = service.abort(execution.execution_id)
    assert updated.status == "aborted"
    assert len(audit.records) == 2


def test_get_execution() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    fetched = service.get_execution(execution.execution_id)
    assert fetched is not None
    assert fetched.execution_id == execution.execution_id


def test_get_missing_execution_raises() -> None:
    service, _ = _make_service()
    with pytest.raises(CallibrError) as exc:
        service.get_execution("nonexistent")
    assert "EXECUTION_NOT_FOUND" in exc.value.code


def test_list_executions() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    e1 = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    e2 = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    executions = service.list_executions("qualification-commerciale")
    assert len(executions) == 2
    assert {e.execution_id for e in executions} == {e1.execution_id, e2.execution_id}


# ---------- Executor edge cases ----------


def test_advance_after_completion_raises() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    service.complete(execution.execution_id)
    with pytest.raises(CallibrError) as exc:
        service.advance(execution.execution_id, AdvanceProcedureRequest(step_id="greeting"))
    assert "INVALID_TRANSITION" in exc.value.code


def test_advance_unknown_step_raises() -> None:
    service, _ = _make_service()
    service.define(SAMPLE_PROCEDURE)
    execution = service.start(StartProcedureRequest(procedure_id="qualification-commerciale"))
    with pytest.raises(CallibrError) as exc:
        service.advance(execution.execution_id, AdvanceProcedureRequest(step_id="unknown"))
    assert "INVALID_TRANSITION" in exc.value.code


# ---------- Validator ----------


def test_validation_duplicate_step_ids() -> None:
    service, _ = _make_service()
    invalid = ProcedureDefinition(
        procedure_id="duplicate-test",
        name="Duplicate Test",
        steps=[
            StepDefinition(step_id="step1", title="Step 1"),
            StepDefinition(step_id="step1", title="Step 1 again"),
        ],
    )
    with pytest.raises(CallibrError) as exc:
        service.define(invalid)
    assert "INVALID_PROCEDURE" in exc.value.code
    assert "duplicate" in str(exc.value.details).lower()


def test_validation_unknown_next_step() -> None:
    service, _ = _make_service()
    invalid = ProcedureDefinition(
        procedure_id="bad-next",
        name="Bad Next",
        steps=[
            StepDefinition(step_id="step1", title="Step 1", next_step="nonexistent"),
        ],
    )
    with pytest.raises(CallibrError) as exc:
        service.define(invalid)
    assert "INVALID_PROCEDURE" in exc.value.code
    assert "unknown next_step" in str(exc.value.details).lower()


# ---------- Procedure with single step ----------


def test_single_step_procedure() -> None:
    service, _ = _make_service()
    single = ProcedureDefinition(
        procedure_id="simple-notification",
        name="Notification unique",
        steps=[StepDefinition(step_id="notify", title="Envoyer notification")],
    )
    service.define(single)
    execution = service.start(StartProcedureRequest(procedure_id="simple-notification"))
    assert execution.status == "running"
    assert execution.current_step_id == "notify"
    updated = service.advance(
        execution.execution_id,
        AdvanceProcedureRequest(step_id="notify", output={"sent": True}),
    )
    assert updated.status == "completed"
