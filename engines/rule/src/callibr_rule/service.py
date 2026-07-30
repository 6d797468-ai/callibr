"""Rule Engine — Declarative business rules layer.

Evaluates rules against execution context.
No runtime effects beyond computing RuleEvaluation.
"""

from __future__ import annotations

from typing import Any

from callibr_contracts import (
    AuditEventStore,
    ExecutionContext,
    RuleDefinition,
    RuleEvaluation,
    RuleExplainResult,
    RuleStore,
    ValidateRuleResult,
)
from callibr_kernel import CallibrError, EventBus

from callibr_rule.evaluator import evaluate_rules, explain_rules
from callibr_rule.events import RuleEvent
from callibr_rule.registry import RuleRegistry
from callibr_rule.validators import RuleValidator


class RuleNotFoundError(CallibrError):
    def __init__(self, rule_id: str) -> None:
        super().__init__(
            "RULE_NOT_FOUND",
            f"Rule {rule_id} was not found.",
            details={"rule_id": rule_id},
        )


class RuleService:
    def __init__(
        self,
        registry: RuleRegistry,
        validator: RuleValidator,
        store: RuleStore,
        audit_event_store: AuditEventStore,
        event_bus: EventBus,
    ) -> None:
        self._registry = registry
        self._validator = validator
        self._store = store
        self._audit_event_store = audit_event_store
        self._event_bus = event_bus

    def define(self, definition: RuleDefinition) -> RuleDefinition:
        result = self._validator.validate(definition)
        if not result.valid:
            raise CallibrError(
                "INVALID_RULE",
                f"Rule validation failed: {'; '.join(result.errors)}",
                details={"errors": result.errors, "warnings": result.warnings},
            )
        self._registry.register(definition)
        self._store.save(definition)
        self._publish(
            "rule.defined",
            definition.rule_id,
            "",
            {
                "name": definition.name,
                "priority": definition.priority,
            },
        )
        return definition

    def get(self, rule_id: str) -> RuleDefinition:
        definition = self._registry.get(rule_id)
        if definition is None:
            definition = self._store.get(rule_id)
            if definition is None:
                raise RuleNotFoundError(rule_id)
            self._registry.register(definition)
        return definition

    def list(self) -> list[RuleDefinition]:
        definitions = self._registry.list()
        if not definitions:
            definitions = self._store.list()
            for d in definitions:
                self._registry.register(d)
        return definitions

    def validate(self, rule_id: str) -> ValidateRuleResult:
        definition = self.get(rule_id)
        result = self._validator.validate(definition)
        self._publish(
            "rule.validated",
            rule_id,
            "",
            {
                "valid": result.valid,
                "error_count": len(result.errors),
            },
        )
        return result

    def evaluate(
        self,
        rules: list[str] | None = None,
        context: ExecutionContext | None = None,
    ) -> RuleEvaluation:
        all_rules = self.list()
        if rules is not None:
            rule_map = {r.rule_id: r for r in all_rules}
            selected = []
            for rid in rules:
                if rid in rule_map:
                    selected.append(rule_map[rid])
        else:
            selected = all_rules

        ctx = context or ExecutionContext()
        evaluation = evaluate_rules(selected, ctx)
        self._publish(
            "rule.evaluated",
            "batch",
            ctx.tenant_id,
            {
                "rule_count": len(selected),
                "matched_count": len(evaluation.matched_rules),
            },
        )
        return evaluation

    def explain(
        self,
        rules: list[str] | None = None,
        context: ExecutionContext | None = None,
    ) -> RuleExplainResult:
        all_rules = self.list()
        if rules is not None:
            rule_map = {r.rule_id: r for r in all_rules}
            selected = []
            for rid in rules:
                if rid in rule_map:
                    selected.append(rule_map[rid])
        else:
            selected = all_rules

        ctx = context or ExecutionContext()
        return explain_rules(selected, ctx)

    def _publish(
        self,
        event_type: str,
        rule_id: str,
        tenant_id: str,
        payload: dict[str, Any],
    ) -> None:
        self._event_bus.publish(
            RuleEvent(
                event_type=event_type,
                rule_id=rule_id,
                tenant_id=tenant_id,
                payload=payload,
            )
        )
