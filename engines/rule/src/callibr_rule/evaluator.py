"""Rule evaluation logic — no side effects, pure computation."""

from __future__ import annotations

from typing import Any

from callibr_contracts import (
    ExecutionContext,
    RuleAction,
    RuleCondition,
    RuleDefinition,
    RuleEvaluation,
    RuleExplainEntry,
    RuleExplainResult,
    RuleMatch,
)


def _eval_condition(cond: RuleCondition, ctx: ExecutionContext) -> bool:
    field_value = ctx.variables.get(cond.field)
    expected = cond.value

    if cond.type == "exists":
        return cond.field in ctx.variables
    if cond.type == "missing":
        return cond.field not in ctx.variables
    if cond.type == "equals":
        return field_value == expected
    if cond.type == "not_equals":
        return field_value != expected
    if cond.type == "greater_than":
        try:
            return bool(field_value is not None and field_value > expected)
        except TypeError:
            return False
    if cond.type == "lower_than":
        try:
            return bool(field_value is not None and field_value < expected)
        except TypeError:
            return False
    if cond.type == "contains":
        try:
            return bool(expected in field_value) if field_value is not None else False
        except TypeError:
            return False
    return False


def _apply_action(
    action: RuleAction,
    variables: dict[str, Any],
    events: list[str],
    score_delta: float,
) -> tuple[dict[str, Any], list[str], float, bool, str]:
    blocked = False
    notes = ""

    if action.type == "set_variable":
        variables[action.target] = action.value
        notes = f"set {action.target}={action.value}"
    elif action.type == "add_score":
        delta = action.value if isinstance(action.value, (int, float)) else 0
        score_delta += delta
        notes = f"score +{delta}"
    elif action.type == "emit_event":
        events.append(str(action.value or action.target))
        notes = f"event {action.value or action.target}"
    elif action.type == "block_transition":
        blocked = True
        notes = "transition blocked"
    elif action.type == "allow":
        notes = "allowed"
    elif action.type == "deny":
        blocked = True
        notes = "denied"
    elif action.type == "advance_step":
        notes = f"advance step to {action.target or 'next'}"

    return variables, events, score_delta, blocked, notes


def evaluate_rules(
    rules: list[RuleDefinition],
    context: ExecutionContext,
) -> RuleEvaluation:
    matched_rules: list[str] = []
    failed_rules: list[str] = []
    matches: list[RuleMatch] = []
    variables: dict[str, Any] = dict(context.variables)
    events: list[str] = []
    total_score: float = 0.0
    warnings: list[str] = []
    blocked = False

    sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    for rule in sorted_rules:
        if not rule.enabled:
            continue

        conditions_met: list[str] = []
        conditions_failed: list[str] = []
        actions_applied: list[str] = []
        score_delta: float = 0.0
        variables_set: dict[str, Any] = {}
        events_emitted: list[str] = []
        justification_parts: list[str] = []

        all_met = True
        for cond in rule.conditions:
            result = _eval_condition(cond, context)
            if result:
                conditions_met.append(cond.condition_id)
                justification_parts.append(f"{cond.field} ({cond.type}) = TRUE")
            else:
                conditions_failed.append(cond.condition_id)
                all_met = False
                justification_parts.append(f"{cond.field} ({cond.type}) = FALSE")

        if all_met:
            matched_rules.append(rule.rule_id)
            for action in rule.actions:
                variables, events, score_delta, act_blocked, notes = _apply_action(
                    action,
                    variables,
                    events,
                    score_delta,
                )
                actions_applied.append(action.action_id)
                if notes:
                    justification_parts.append(f"action {action.type}: {notes}")
                if act_blocked:
                    blocked = True
                    justification_parts.append("BLOCKED")
                if action.type == "set_variable":
                    variables_set[action.target] = action.value
                if action.type == "emit_event":
                    events_emitted.append(str(action.value or action.target))
            total_score += score_delta
        else:
            failed_rules.append(rule.rule_id)

        matches.append(
            RuleMatch(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                matched=all_met,
                priority=rule.priority,
                conditions_met=conditions_met,
                conditions_failed=conditions_failed,
                actions_applied=actions_applied,
                score_delta=score_delta,
                variables_set=variables_set,
                events_emitted=events_emitted,
                justification="; ".join(justification_parts),
            )
        )

    return RuleEvaluation(
        results=matches,
        matched_rules=matched_rules,
        failed_rules=failed_rules,
        total_score_delta=total_score,
        variables=variables,
        events=events,
        warnings=warnings,
        blocked=blocked,
    )


def explain_rules(
    rules: list[RuleDefinition],
    context: ExecutionContext,
) -> RuleExplainResult:
    entries: list[RuleExplainEntry] = []

    sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    for rule in sorted_rules:
        cond_details: list[dict[str, Any]] = []
        for cond in rule.conditions:
            result = _eval_condition(cond, context)
            cond_details.append(
                {
                    "condition_id": cond.condition_id,
                    "type": cond.type,
                    "field": cond.field,
                    "expected": cond.value,
                    "actual": context.variables.get(cond.field),
                    "result": result,
                }
            )

        action_details: list[dict[str, Any]] = [
            {
                "action_id": a.action_id,
                "type": a.type,
                "target": a.target,
                "value": a.value,
            }
            for a in rule.actions
        ]

        all_met = all(_eval_condition(cond, context) for cond in rule.conditions)
        parts: list[str] = []
        for cd in cond_details:
            parts.append(f"{cd['field']} ({cd['type']}) = {cd['result']}")
        justification = "; ".join(parts)

        entries.append(
            RuleExplainEntry(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                priority=rule.priority,
                enabled=rule.enabled,
                matched=all_met,
                conditions=cond_details,
                actions=action_details,
                justification=justification,
            )
        )

    return RuleExplainResult(
        context=context,
        entries=entries,
    )
