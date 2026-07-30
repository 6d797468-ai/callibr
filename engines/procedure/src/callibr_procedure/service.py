from __future__ import annotations

from typing import Any

from callibr_contracts import (
    AdvanceProcedureRequest,
    AuditEventStore,
    AuditRecord,
    ProcedureDefinition,
    ProcedureExecution,
    ProcedureStore,
    ProcedureSummary,
    StartProcedureRequest,
)
from callibr_kernel import CallibrError, EventBus, new_id, new_trace_id, utc_now

from callibr_procedure.events import ProcedureEvent
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_procedure.validators import validate_procedure


class ProcedureNotFoundError(CallibrError):
    def __init__(self, procedure_id: str) -> None:
        super().__init__(
            "PROCEDURE_NOT_FOUND",
            f"Procedure {procedure_id} was not found.",
            details={"procedure_id": procedure_id},
        )


class ExecutionNotFoundError(CallibrError):
    def __init__(self, execution_id: str) -> None:
        super().__init__(
            "EXECUTION_NOT_FOUND",
            f"Execution {execution_id} was not found.",
            details={"execution_id": execution_id},
        )


class ProcedureService:
    def __init__(
        self,
        registry: ProcedureRegistry,
        executor: ProcedureExecutor,
        store: ProcedureStore,
        audit_event_store: AuditEventStore,
        event_bus: EventBus,
    ) -> None:
        self._registry = registry
        self._executor = executor
        self._store = store
        self._audit_event_store = audit_event_store
        self._event_bus = event_bus

    def define(self, definition: ProcedureDefinition) -> ProcedureDefinition:
        errors = validate_procedure(definition)
        if errors:
            raise CallibrError(
                "INVALID_PROCEDURE",
                f"Procedure validation failed: {'; '.join(errors)}",
                details={"errors": errors},
            )
        self._registry.register(definition)
        self._store.save_definition(definition)
        self._event_bus.publish(
            ProcedureEvent(
                event_type="procedure.defined",
                execution_id="",
                tenant_id="",
                procedure_id=definition.procedure_id,
                payload={"name": definition.name, "step_count": len(definition.steps)},
            )
        )
        return definition

    def get_procedure(self, procedure_id: str) -> ProcedureDefinition:
        procedure = self._registry.get(procedure_id)
        if procedure is None:
            procedure = self._store.get_definition(procedure_id)
            if procedure is None:
                raise ProcedureNotFoundError(procedure_id)
            self._registry.register(procedure)
        return procedure

    def list_procedures(self) -> list[ProcedureSummary]:
        definitions = self._registry.list()
        if not definitions:
            definitions = self._store.list_definitions()
            for d in definitions:
                self._registry.register(d)
        return [
            ProcedureSummary(
                procedure_id=d.procedure_id,
                name=d.name,
                version=d.version,
                description=d.description,
                step_count=len(d.steps),
            )
            for d in definitions
        ]

    def start(self, request: StartProcedureRequest) -> ProcedureExecution:
        procedure = self.get_procedure(request.procedure_id)
        execution = self._executor.start(
            procedure=procedure,
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            initial_context=request.initial_context,
        )
        self._store.save_execution(execution)
        self._append_audit(
            "procedure.started",
            execution,
            request.tenant_id,
            request.actor_id,
            {
                "procedure_id": procedure.procedure_id,
                "first_step": execution.current_step_id,
            },
        )
        self._event_bus.publish(
            ProcedureEvent(
                event_type="procedure.started",
                execution_id=execution.execution_id,
                tenant_id=request.tenant_id,
                procedure_id=procedure.procedure_id,
                payload={"first_step": execution.current_step_id},
            )
        )
        return execution

    def advance(
        self,
        execution_id: str,
        request: AdvanceProcedureRequest,
    ) -> ProcedureExecution:
        execution = self._get_execution(execution_id)
        procedure = self.get_procedure(execution.procedure_id)

        try:
            updated = self._executor.advance(execution, procedure, request.step_id, request.output)
        except Exception as e:
            raise CallibrError(
                "INVALID_TRANSITION",
                str(e),
                details={"execution_id": execution_id, "step_id": request.step_id},
            ) from e
        self._store.save_execution(updated)
        self._append_audit(
            "procedure.step_completed",
            updated,
            execution.tenant_id,
            updated.context.get("actor_id", "system"),
            {
                "step_id": request.step_id,
                "next_step": updated.current_step_id,
                "status": updated.status,
            },
        )
        if updated.status == "completed":
            self._event_bus.publish(
                ProcedureEvent(
                    event_type="procedure.completed",
                    execution_id=updated.execution_id,
                    tenant_id=execution.tenant_id,
                    procedure_id=procedure.procedure_id,
                    payload={
                        "score": updated.score,
                        "elapsed_seconds": updated.elapsed_seconds,
                    },
                )
            )
        return updated

    def fail(self, execution_id: str, step_id: str, error: str) -> ProcedureExecution:
        execution = self._get_execution(execution_id)
        updated = self._executor.fail(execution, step_id, error)
        self._store.save_execution(updated)
        self._append_audit(
            "procedure.step_failed",
            updated,
            execution.tenant_id,
            updated.context.get("actor_id", "system"),
            {"step_id": step_id, "error": error},
        )
        self._event_bus.publish(
            ProcedureEvent(
                event_type="procedure.failed",
                execution_id=updated.execution_id,
                tenant_id=execution.tenant_id,
                procedure_id=execution.procedure_id,
                payload={"step_id": step_id, "error": error},
            )
        )
        return updated

    def complete(self, execution_id: str, score: int | None = None) -> ProcedureExecution:
        execution = self._get_execution(execution_id)
        updated = self._executor.complete(execution, score)
        self._store.save_execution(updated)
        self._append_audit(
            "procedure.manually_completed",
            updated,
            execution.tenant_id,
            updated.context.get("actor_id", "system"),
            {"final_score": updated.score},
        )
        return updated

    def abort(self, execution_id: str) -> ProcedureExecution:
        execution = self._get_execution(execution_id)
        updated = self._executor.abort(execution)
        self._store.save_execution(updated)
        self._append_audit(
            "procedure.aborted",
            updated,
            execution.tenant_id,
            updated.context.get("actor_id", "system"),
            {},
        )
        return updated

    def get_execution(self, execution_id: str) -> ProcedureExecution:
        return self._get_execution(execution_id)

    def list_executions(self, procedure_id: str) -> list[ProcedureExecution]:
        return self._store.list_executions(procedure_id)

    def _get_execution(self, execution_id: str) -> ProcedureExecution:
        execution = self._executor.get_execution(execution_id)
        if execution is None:
            execution = self._store.get_execution(execution_id)
            if execution is None:
                raise ExecutionNotFoundError(execution_id)
        return execution

    def _append_audit(
        self,
        event_type: str,
        execution: ProcedureExecution,
        tenant_id: str,
        actor_id: str | None,
        payload: dict[str, Any],
    ) -> None:
        self._audit_event_store.append(
            AuditRecord(
                audit_id=new_id("audit"),
                event_type=event_type,
                tenant_id=tenant_id,
                aggregate_type="procedure_execution",
                aggregate_id=execution.execution_id,
                occurred_at=utc_now(),
                trace_id=new_trace_id(),
                actor_id=actor_id or "system",
                payload=payload,
            )
        )
