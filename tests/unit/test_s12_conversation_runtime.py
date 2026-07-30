"""Tests unitaires — S12 Conversation Runtime.

Couvre :
- Module seed : chargement du catalogue de référence
- ProcedureExecutor : auto-avancement par order quand next_step absent
- PersonaTrait : nouveaux traits client dans l'enum TraitName
- ProcedureService._append_audit : instanciation correcte d'AuditRecord
"""

from __future__ import annotations

import pytest
from callibr_contracts import (
    PersonaTrait,
    ProcedureDefinition,
    StartProcedureRequest,
    StepDefinition,
)
from callibr_kernel import EventBus
from callibr_persistence import (
    InMemoryAuditEventStore,
    InMemoryPersonaDefinitionStore,
    InMemoryProcedureStore,
    InMemoryRuleStore,
    InMemoryScenarioDefinitionStore,
)
from callibr_persona import PersonaRegistry, PersonaService, PersonaValidator
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_rule import RuleRegistry, RuleService, RuleValidator
from callibr_scenario import ScenarioRegistry, ScenarioService, ScenarioValidator
from callibr_seed import load_demo_catalogue

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_procedure_service() -> ProcedureService:
    return ProcedureService(
        registry=ProcedureRegistry(),
        executor=ProcedureExecutor(),
        store=InMemoryProcedureStore(),
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
    )


def _make_persona_service() -> PersonaService:
    return PersonaService(
        registry=PersonaRegistry(),
        validator=PersonaValidator(),
        store=InMemoryPersonaDefinitionStore(),
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
    )


def _make_rule_service() -> RuleService:
    return RuleService(
        registry=RuleRegistry(),
        validator=RuleValidator(),
        store=InMemoryRuleStore(),
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
    )


def _make_scenario_service(procedure_service: ProcedureService) -> ScenarioService:
    return ScenarioService(
        registry=ScenarioRegistry(),
        validator=ScenarioValidator(
            procedure_registry=procedure_service._registry,
            procedure_store=None,
        ),
        store=InMemoryScenarioDefinitionStore(),
        procedure_service=procedure_service,
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
    )


# ---------------------------------------------------------------------------
# Seed catalogue
# ---------------------------------------------------------------------------


class TestSeedCatalogue:
    def test_load_demo_catalogue_populates_all_stores(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        load_demo_catalogue(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )

        assert len(persona_svc.list()) == 8
        assert len(proc_svc.list_procedures()) == 8
        assert len(rule_svc.list()) == 2
        assert len(scenario_svc.list()) == 8

    def test_load_demo_catalogue_is_idempotent(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        kwargs = dict(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )
        load_demo_catalogue(**kwargs)
        load_demo_catalogue(**kwargs)  # second call must not raise

        assert len(persona_svc.list()) == 8

    def test_seeded_persona_has_client_traits(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        load_demo_catalogue(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )

        persona = persona_svc.get("persona-sav-client-frustre-001")
        trait_names = {t.name for t in persona.traits}
        assert "frustration" in trait_names
        assert "coopération" in trait_names

    def test_seeded_procedure_has_five_ordered_steps(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        load_demo_catalogue(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )

        proc = proc_svc.get_procedure("proc-sav-retard-colis-001")
        assert len(proc.steps) == 5
        orders = [s.order for s in proc.steps]
        assert orders == [1, 2, 3, 4, 5]

    def test_seeded_rule_blocks_when_identity_not_verified(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        load_demo_catalogue(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )

        from callibr_contracts import ExecutionContext

        ctx = ExecutionContext(variables={"identity_verified": False})
        evaluation = rule_svc.evaluate(context=ctx)
        assert evaluation.blocked is True
        assert "rule-identity-required" in evaluation.matched_rules

    def test_seeded_scenario_references_correct_procedure_and_persona(self) -> None:
        proc_svc = _make_procedure_service()
        persona_svc = _make_persona_service()
        rule_svc = _make_rule_service()
        scenario_svc = _make_scenario_service(proc_svc)

        load_demo_catalogue(
            persona_service=persona_svc,
            procedure_service=proc_svc,
            rule_service=rule_svc,
            scenario_service=scenario_svc,
        )

        scenario = scenario_svc.get("sc-sav-retard-colis-v1")
        assert scenario.reference.procedure_id == "proc-sav-retard-colis-001"
        assert scenario.reference.persona_id == "persona-sav-client-frustre-001"


# ---------------------------------------------------------------------------
# ProcedureExecutor — auto-advance par order
# ---------------------------------------------------------------------------


class TestProcedureExecutorAutoAdvance:
    def _make_procedure(self) -> ProcedureDefinition:
        return ProcedureDefinition(
            procedure_id="proc-test",
            name="Test Procedure",
            steps=[
                StepDefinition(step_id="s1", title="Step 1", order=1),
                StepDefinition(step_id="s2", title="Step 2", order=2),
                StepDefinition(step_id="s3", title="Step 3", order=3),
            ],
        )

    def test_advance_by_order_moves_to_next_step(self) -> None:
        executor = ProcedureExecutor()
        procedure = self._make_procedure()
        execution = executor.start(procedure, "tenant_demo", "learner_demo")

        assert execution.current_step_id == "s1"

        updated = executor.advance(execution, procedure, "s1", {})

        assert updated.current_step_id == "s2"
        assert "s1" in updated.completed_step_ids
        assert updated.status == "running"

    def test_advance_through_all_steps_completes_execution(self) -> None:
        executor = ProcedureExecutor()
        procedure = self._make_procedure()
        execution = executor.start(procedure, "tenant_demo", "learner_demo")

        e1 = executor.advance(execution, procedure, "s1", {})
        e2 = executor.advance(e1, procedure, "s2", {})
        e3 = executor.advance(e2, procedure, "s3", {})

        assert e3.status == "completed"
        assert e3.current_step_id is None
        assert set(e3.completed_step_ids) == {"s1", "s2", "s3"}

    def test_explicit_next_step_takes_priority_over_order(self) -> None:
        procedure = ProcedureDefinition(
            procedure_id="proc-jump",
            name="Jump Procedure",
            steps=[
                StepDefinition(step_id="s1", title="Step 1", order=1, next_step="s3"),
                StepDefinition(step_id="s2", title="Step 2", order=2),
                StepDefinition(step_id="s3", title="Step 3", order=3),
            ],
        )
        executor = ProcedureExecutor()
        execution = executor.start(procedure, "tenant_demo", "learner_demo")

        updated = executor.advance(execution, procedure, "s1", {})

        # s1 has next_step="s3" — should skip s2
        assert updated.current_step_id == "s3"

    def test_steps_without_order_do_not_auto_advance(self) -> None:
        procedure = ProcedureDefinition(
            procedure_id="proc-no-order",
            name="No Order Procedure",
            steps=[
                StepDefinition(step_id="s1", title="Step 1"),  # no order
                StepDefinition(step_id="s2", title="Step 2"),  # no order
            ],
        )
        executor = ProcedureExecutor()
        execution = executor.start(procedure, "tenant_demo", "learner_demo")

        updated = executor.advance(execution, procedure, "s1", {})

        # No order, no next_step → execution completes immediately
        assert updated.status == "completed"
        assert updated.current_step_id is None


# ---------------------------------------------------------------------------
# PersonaTrait — traits client élargis
# ---------------------------------------------------------------------------


class TestPersonaTraitClientEnum:
    @pytest.mark.parametrize(
        "trait_name",
        [
            "frustration",
            "coopération",
            "exigence",
            "anxiété",
            "satisfaction",
            "impatience",
        ],
    )
    def test_client_trait_accepted_by_pydantic(self, trait_name: str) -> None:
        trait = PersonaTrait(trait_id=f"t-{trait_name}", name=trait_name, weight=0.8)
        assert trait.name == trait_name

    def test_unknown_trait_raises_validation_error(self) -> None:
        import pydantic

        with pytest.raises(pydantic.ValidationError):
            PersonaTrait(trait_id="t-bad", name="unknown_trait", weight=1.0)


# ---------------------------------------------------------------------------
# ProcedureService._append_audit — AuditRecord réel
# ---------------------------------------------------------------------------


class TestProcedureServiceAuditRecord:
    def test_audit_records_are_real_pydantic_models(self) -> None:
        from callibr_contracts import AuditRecord

        proc_svc = _make_procedure_service()
        definition = ProcedureDefinition(
            procedure_id="proc-audit-test",
            name="Audit Test",
            steps=[StepDefinition(step_id="s1", title="Step One", order=1)],
        )
        proc_svc.define(definition)
        execution = proc_svc.start(StartProcedureRequest(procedure_id="proc-audit-test"))

        audit_store = proc_svc._audit_event_store
        records = audit_store.list_by_aggregate("procedure_execution", execution.execution_id)

        assert len(records) == 1
        record = records[0]
        assert isinstance(record, AuditRecord), f"Expected AuditRecord, got {type(record)}"
        assert record.event_type == "procedure.started"
        assert record.aggregate_id == execution.execution_id
