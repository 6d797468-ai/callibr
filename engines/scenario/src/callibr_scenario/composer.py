"""Scenario Engine — Composition Layer.

Prepares execution plans from declarative definitions.
No runtime logic. Calls ProcedureService to launch.
"""

from __future__ import annotations

from typing import Any

from callibr_contracts import (
    AuditEventStore,
    ProcedureDefinition,
    ProcedureExecution,
    ProcedureStore,
    ScenarioDefinition,
    ScenarioDefinitionStore,
    ScenarioExecutionPlan,
    ScenarioExecutionResult,
    StartProcedureRequest,
    ValidateScenarioResult,
)
from callibr_kernel import CallibrError, EventBus, new_id, utc_now
from callibr_procedure import ProcedureService
from callibr_procedure.registry import ProcedureRegistry

from callibr_scenario.events import ScenarioEvent


class ScenarioNotFoundError(CallibrError):
    def __init__(self, scenario_id: str) -> None:
        super().__init__(
            "SCENARIO_NOT_FOUND",
            f"Scenario {scenario_id} was not found.",
            details={"scenario_id": scenario_id},
        )


class ScenarioRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, ScenarioDefinition] = {}

    def register(self, definition: ScenarioDefinition) -> None:
        self._definitions[definition.scenario_id] = definition

    def get(self, scenario_id: str) -> ScenarioDefinition | None:
        return self._definitions.get(scenario_id)

    def list(self) -> list[ScenarioDefinition]:
        return list(self._definitions.values())

    def remove(self, scenario_id: str) -> None:
        self._definitions.pop(scenario_id, None)


class ScenarioValidator:
    def __init__(
        self,
        procedure_registry: ProcedureRegistry | None = None,
        procedure_store: ProcedureStore | None = None,
    ) -> None:
        self._procedure_registry = procedure_registry
        self._procedure_store = procedure_store

    def validate(
        self,
        definition: ScenarioDefinition,
    ) -> ValidateScenarioResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not definition.scenario_id:
            errors.append("scenario_id is required")
        if not definition.name:
            errors.append("name is required")

        ref = definition.reference
        if not ref.procedure_id:
            errors.append("reference.procedure_id is required")
        else:
            procedure = self._find_procedure(ref.procedure_id)
            if procedure is None:
                errors.append(f"procedure '{ref.procedure_id}' not found")
            elif ref.procedure_version and procedure.version != ref.procedure_version:
                warnings.append(
                    f"procedure '{ref.procedure_id}' version mismatch: "
                    f"expected {ref.procedure_version}, found {procedure.version}"
                )

        if not ref.persona_id:
            errors.append("reference.persona_id is required")

        if not definition.objectives:
            warnings.append("no objectives defined")

        return ValidateScenarioResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _find_procedure(self, procedure_id: str) -> ProcedureDefinition | None:
        if self._procedure_registry:
            proc = self._procedure_registry.get(procedure_id)
            if proc:
                return proc
        if self._procedure_store:
            return self._procedure_store.get_definition(procedure_id)
        return None


class ScenarioService:
    def __init__(
        self,
        registry: ScenarioRegistry,
        validator: ScenarioValidator,
        store: ScenarioDefinitionStore,
        procedure_service: ProcedureService,
        audit_event_store: AuditEventStore,
        event_bus: EventBus,
    ) -> None:
        self._registry = registry
        self._validator = validator
        self._store = store
        self._procedure_service = procedure_service
        self._audit_event_store = audit_event_store
        self._event_bus = event_bus

    def define(self, definition: ScenarioDefinition) -> ScenarioDefinition:
        result = self._validator.validate(definition)
        if not result.valid:
            raise CallibrError(
                "INVALID_SCENARIO",
                f"Scenario validation failed: {'; '.join(result.errors)}",
                details={"errors": result.errors, "warnings": result.warnings},
            )
        self._registry.register(definition)
        self._store.save(definition)
        self._publish(
            "scenario.defined",
            definition.scenario_id,
            "",
            "",
            {
                "name": definition.name,
                "procedure_id": definition.reference.procedure_id,
            },
        )
        return definition

    def get(self, scenario_id: str) -> ScenarioDefinition:
        definition = self._registry.get(scenario_id)
        if definition is None:
            definition = self._store.get(scenario_id)
            if definition is None:
                raise ScenarioNotFoundError(scenario_id)
            self._registry.register(definition)
        return definition

    def list(self) -> list[ScenarioDefinition]:
        definitions = self._registry.list()
        if not definitions:
            definitions = self._store.list()
            for d in definitions:
                self._registry.register(d)
        return definitions

    def validate(self, scenario_id: str) -> ValidateScenarioResult:
        definition = self.get(scenario_id)
        result = self._validator.validate(definition)
        self._publish(
            "scenario.validated",
            scenario_id,
            "",
            "",
            {
                "valid": result.valid,
                "error_count": len(result.errors),
            },
        )
        return result

    def compose(
        self,
        scenario_id: str,
        tenant_id: str = "tenant_demo",
        actor_id: str = "learner_demo",
        extra_context: dict[str, Any] | None = None,
    ) -> ScenarioExecutionPlan:
        definition = self.get(scenario_id)
        now = utc_now()
        plan = ScenarioExecutionPlan(
            plan_id=new_id("plan"),
            scenario=definition,
            execution_context={
                "actor_id": actor_id,
                "tenant_id": tenant_id,
                "procedure_id": definition.reference.procedure_id,
                "persona_id": definition.reference.persona_id,
                "crm_context_key": definition.reference.crm_context_key,
                "rule_ids": list(definition.reference.rule_ids),
                "objectives": [
                    {"id": o.objective_id, "label": o.label} for o in definition.objectives
                ],
                "difficulty": definition.metadata.difficulty,
                "estimated_minutes": definition.metadata.estimated_minutes,
                **(extra_context or {}),
            },
            composed_at=now,
            tenant_id=tenant_id,
            actor_id=actor_id,
        )
        self._publish(
            "scenario.composed",
            scenario_id,
            plan.plan_id,
            tenant_id,
            {
                "procedure_id": definition.reference.procedure_id,
                "persona_id": definition.reference.persona_id,
            },
        )
        return plan

    def launch(
        self,
        plan: ScenarioExecutionPlan,
    ) -> ScenarioExecutionResult:
        request = StartProcedureRequest(
            procedure_id=plan.scenario.reference.procedure_id,
            tenant_id=plan.tenant_id,
            actor_id=plan.actor_id,
            initial_context=plan.execution_context,
        )
        execution: ProcedureExecution = self._procedure_service.start(request)
        self._publish(
            "scenario.launched",
            plan.scenario.scenario_id,
            plan.plan_id,
            plan.tenant_id,
            {
                "execution_id": execution.execution_id,
                "procedure_id": execution.procedure_id,
            },
        )
        self._append_audit(
            "scenario.launched",
            plan,
            execution.execution_id,
        )
        return ScenarioExecutionResult(
            plan=plan,
            execution_id=execution.execution_id,
            status=execution.status,
            procedure_id=execution.procedure_id,
        )

    def _publish(
        self,
        event_type: str,
        scenario_id: str,
        plan_id: str,
        tenant_id: str,
        payload: dict[str, Any],
    ) -> None:
        self._event_bus.publish(
            ScenarioEvent(
                event_type=event_type,
                scenario_id=scenario_id,
                plan_id=plan_id,
                tenant_id=tenant_id,
                payload=payload,
            )
        )

    def _append_audit(
        self,
        event_type: str,
        plan: ScenarioExecutionPlan,
        execution_id: str,
    ) -> None:
        self._audit_event_store.append(
            type(
                "AuditRecord",
                (),
                {
                    "audit_id": f"audit_{utc_now().timestamp()}",
                    "event_type": event_type,
                    "tenant_id": plan.tenant_id,
                    "aggregate_type": "scenario_execution",
                    "aggregate_id": execution_id,
                    "occurred_at": utc_now(),
                    "trace_id": "",
                    "actor_id": plan.actor_id,
                    "payload": {
                        "scenario_id": plan.scenario.scenario_id,
                        "plan_id": plan.plan_id,
                    },
                },
            )()
        )
