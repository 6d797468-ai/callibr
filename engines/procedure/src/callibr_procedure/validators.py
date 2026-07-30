from __future__ import annotations

from typing import Any

from callibr_contracts import ProcedureDefinition, StepDefinition


class ValidationError(Exception):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


def validate_procedure(procedure: ProcedureDefinition) -> list[str]:
    errors: list[str] = []

    if not procedure.procedure_id:
        errors.append("procedure_id is required")
    if not procedure.name:
        errors.append("name is required")
    if not procedure.steps:
        errors.append("at least one step is required")

    step_ids = set()
    for step in procedure.steps:
        _validate_step(step, errors, step_ids)

    for step in procedure.steps:
        if step.next_step and step.next_step not in step_ids:
            errors.append(f"step '{step.step_id}' references unknown next_step '{step.next_step}'")

    return errors


def _validate_step(step: StepDefinition, errors: list[str], step_ids: set[str]) -> None:
    if not step.step_id:
        errors.append("each step must have a step_id")
        return
    if step.step_id in step_ids:
        errors.append(f"duplicate step_id '{step.step_id}'")
    step_ids.add(step.step_id)

    if not step.title:
        errors.append(f"step '{step.step_id}' is missing a title")
