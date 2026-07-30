from __future__ import annotations

from typing import Any

from callibr_contracts import (
    ProcedureDefinition,
    ProcedureExecution,
    StepResult,
)
from callibr_kernel import new_id, utc_now


class ExecutionNotFoundError(Exception):
    pass


class InvalidTransitionError(Exception):
    pass


class ProcedureExecutor:
    def __init__(self) -> None:
        self._executions: dict[str, ProcedureExecution] = {}

    def start(
        self,
        procedure: ProcedureDefinition,
        tenant_id: str,
        actor_id: str,
        initial_context: dict[str, Any] | None = None,
    ) -> ProcedureExecution:
        now = utc_now()
        first_step = procedure.steps[0]
        execution = ProcedureExecution(
            execution_id=new_id("proc_exec"),
            tenant_id=tenant_id,
            procedure_id=procedure.procedure_id,
            procedure_version=procedure.version,
            status="running",
            current_step_id=first_step.step_id,
            steps=[
                StepResult(
                    step_id=first_step.step_id,
                    status="active",
                    started_at=now,
                )
            ],
            started_at=now,
            context={
                "actor_id": actor_id,
                **(initial_context or {}),
            },
        )
        self._executions[execution.execution_id] = execution
        return execution

    def advance(
        self,
        execution: ProcedureExecution,
        procedure: ProcedureDefinition,
        step_id: str,
        output: dict[str, Any] | None = None,
    ) -> ProcedureExecution:
        if execution.status != "running":
            raise InvalidTransitionError(
                f"Cannot advance execution '{execution.execution_id}' "
                f"in status '{execution.status}'"
            )

        now = utc_now()
        step_map = procedure.step_map()
        current_step_def = step_map.get(step_id)
        if current_step_def is None:
            raise InvalidTransitionError(
                f"Step '{step_id}' not found in procedure '{procedure.procedure_id}'"
            )

        completed = [
            StepResult(
                step_id=s.step_id,
                status="completed" if s.step_id == step_id else s.status,
                started_at=s.started_at,
                completed_at=now if s.step_id == step_id else s.completed_at,
                score=s.score,
                output=output if s.step_id == step_id else s.output,
            )
            if s.step_id == step_id
            else s
            for s in execution.steps
        ]

        next_step_id = current_step_def.next_step
        if next_step_id is None:
            # Fallback: advance by ascending `order` when `next_step` is not
            # explicitly declared. Steps without an `order` field are treated
            # as order=0 and will not be auto-advanced into.
            current_order = getattr(current_step_def, "order", None)
            if current_order is not None:
                candidates = sorted(
                    (
                        s
                        for s in procedure.steps
                        if getattr(s, "order", None) is not None
                        and s.order > current_order  # type: ignore[operator]
                        and s.step_id
                        not in {r.step_id for r in completed if r.status == "completed"}
                    ),
                    key=lambda s: s.order,  # type: ignore[attr-defined]
                )
                if candidates:
                    next_step_id = candidates[0].step_id

        if next_step_id:
            next_def = step_map.get(next_step_id)
            if next_def:
                completed.append(
                    StepResult(
                        step_id=next_step_id,
                        status="active",
                        started_at=now,
                    )
                )

        elapsed = int((now - execution.started_at).total_seconds())
        status = "completed" if next_step_id is None else "running"

        updated = execution.model_copy(
            update={
                "status": status,
                "current_step_id": next_step_id,
                "completed_step_ids": [s.step_id for s in completed if s.status == "completed"],
                "steps": completed,
                "completed_at": now if status == "completed" else None,
                "elapsed_seconds": elapsed,
                "context": {**execution.context, **(output or {})},
            }
        )
        self._executions[execution.execution_id] = updated
        return updated

    def fail(
        self,
        execution: ProcedureExecution,
        step_id: str,
        error: str,
    ) -> ProcedureExecution:
        now = utc_now()
        failed_steps = [
            StepResult(
                step_id=s.step_id,
                status="failed" if s.step_id == step_id else s.status,
                started_at=s.started_at,
                completed_at=now if s.step_id == step_id else s.completed_at,
                score=s.score,
                error=error if s.step_id == step_id else s.error,
            )
            if s.step_id == step_id
            else s
            for s in execution.steps
        ]

        updated = execution.model_copy(
            update={
                "status": "failed",
                "current_step_id": step_id,
                "steps": failed_steps,
                "completed_at": now,
                "elapsed_seconds": int((now - execution.started_at).total_seconds()),
            }
        )
        self._executions[execution.execution_id] = updated
        return updated

    def complete(
        self,
        execution: ProcedureExecution,
        score: int | None = None,
    ) -> ProcedureExecution:
        now = utc_now()
        final_score = score if score is not None else execution.score
        completed_steps = [
            StepResult(
                step_id=s.step_id,
                status="completed" if s.status in ("active", "pending") else s.status,
                started_at=s.started_at,
                completed_at=s.completed_at or now,
                score=s.score,
            )
            for s in execution.steps
        ]

        updated = execution.model_copy(
            update={
                "status": "completed",
                "current_step_id": None,
                "completed_step_ids": [s.step_id for s in completed_steps],
                "steps": completed_steps,
                "completed_at": now,
                "elapsed_seconds": int((now - execution.started_at).total_seconds()),
                "score": final_score,
            }
        )
        self._executions[execution.execution_id] = updated
        return updated

    def abort(self, execution: ProcedureExecution) -> ProcedureExecution:
        now = utc_now()
        aborted_steps = [
            StepResult(
                step_id=s.step_id,
                status="skipped" if s.status in ("active", "pending") else s.status,
                started_at=s.started_at,
                completed_at=s.completed_at,
                score=s.score,
            )
            for s in execution.steps
        ]

        updated = execution.model_copy(
            update={
                "status": "aborted",
                "current_step_id": None,
                "steps": aborted_steps,
                "completed_at": now,
                "elapsed_seconds": int((now - execution.started_at).total_seconds()),
            }
        )
        self._executions[execution.execution_id] = updated
        return updated

    def get_execution(self, execution_id: str) -> ProcedureExecution | None:
        return self._executions.get(execution_id)

    def list_executions(self, procedure_id: str) -> list[ProcedureExecution]:
        return [e for e in self._executions.values() if e.procedure_id == procedure_id]
