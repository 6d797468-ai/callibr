from __future__ import annotations

from callibr_contracts import (
    RuleDefinition,
    ValidateRuleResult,
)

_CONDITION_TYPES = {
    "equals",
    "not_equals",
    "exists",
    "missing",
    "greater_than",
    "lower_than",
    "contains",
}
_ACTION_TYPES = {
    "allow",
    "deny",
    "set_variable",
    "add_score",
    "emit_event",
    "advance_step",
    "block_transition",
}


class RuleValidator:
    def validate(self, definition: RuleDefinition) -> ValidateRuleResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not definition.rule_id:
            errors.append("rule_id is required")
        if not definition.name:
            errors.append("name is required")

        self._validate_conditions(definition, errors, warnings)
        self._validate_actions(definition, errors, warnings)
        self._validate_constraints(definition, errors, warnings)
        self._validate_metadata(definition, errors, warnings)

        return ValidateRuleResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_conditions(
        self,
        definition: RuleDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        if not definition.conditions:
            warnings.append("no conditions defined — rule will always match")
            return
        seen: set[str] = set()
        for cond in definition.conditions:
            if not cond.condition_id:
                errors.append("each condition must have a condition_id")
                continue
            if cond.condition_id in seen:
                errors.append(f"duplicate condition_id '{cond.condition_id}'")
            seen.add(cond.condition_id)
            if cond.type not in _CONDITION_TYPES:
                errors.append(f"condition '{cond.condition_id}' has unknown type '{cond.type}'")
            if not cond.field:
                errors.append(f"condition '{cond.condition_id}' is missing a field")

    def _validate_actions(
        self,
        definition: RuleDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        if not definition.actions:
            warnings.append("no actions defined — rule will have no effect")
            return
        seen: set[str] = set()
        for action in definition.actions:
            if not action.action_id:
                errors.append("each action must have an action_id")
                continue
            if action.action_id in seen:
                errors.append(f"duplicate action_id '{action.action_id}'")
            seen.add(action.action_id)
            if action.type not in _ACTION_TYPES:
                errors.append(f"action '{action.action_id}' has unknown type '{action.type}'")

    def _validate_constraints(
        self,
        definition: RuleDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        seen: set[str] = set()
        for constraint in definition.constraints:
            if not constraint.constraint_id:
                errors.append("each constraint must have a constraint_id")
                continue
            if constraint.constraint_id in seen:
                errors.append(f"duplicate constraint_id '{constraint.constraint_id}'")
            seen.add(constraint.constraint_id)

    def _validate_metadata(
        self,
        definition: RuleDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        pass
