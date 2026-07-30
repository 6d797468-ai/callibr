from __future__ import annotations

from typing import Any

import pytest
from callibr_contracts import (
    AuditRecord,
    ExecutionContext,
    RuleAction,
    RuleCondition,
    RuleDefinition,
)
from callibr_kernel import EventBus
from callibr_rule import (
    RuleNotFoundError,
    RuleRegistry,
    RuleService,
    RuleValidator,
)
from callibr_rule.evaluator import evaluate_rules


class _InMemoryAuditStore:
    def __init__(self) -> None:
        self.records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self.records.append(record)

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[AuditRecord]:
        return [
            r
            for r in self.records
            if r.aggregate_type == aggregate_type and r.aggregate_id == aggregate_id
        ]


class _InMemoryRuleStore:
    def __init__(self) -> None:
        self._store: dict[str, RuleDefinition] = {}

    def save(self, definition: RuleDefinition) -> None:
        self._store[definition.rule_id] = definition

    def get(self, rule_id: str) -> RuleDefinition | None:
        return self._store.get(rule_id)

    def list(self) -> list[RuleDefinition]:
        return list(self._store.values())


def _valid_rule(**overrides: Any) -> RuleDefinition:
    kwargs: dict[str, Any] = {
        "rule_id": "qualification-budget",
        "name": "Qualification Budget",
        "description": "Vérifie la qualification du budget",
        "priority": 100,
        "enabled": True,
        "conditions": [
            RuleCondition(
                condition_id="budget-known",
                type="exists",
                field="budget_known",
                label="Budget connu",
            ),
            RuleCondition(
                condition_id="dm-identified",
                type="equals",
                field="decision_maker_identified",
                value=True,
                label="Décideur identifié",
            ),
        ],
        "actions": [
            RuleAction(
                action_id="add-score",
                type="add_score",
                value=10.0,
                label="Ajouter score",
            ),
            RuleAction(
                action_id="unlock-next",
                type="advance_step",
                label="Débloquer étape suivante",
            ),
        ],
    }
    kwargs.update(overrides)
    return RuleDefinition(**kwargs)


def _make_service() -> tuple[RuleService, _InMemoryAuditStore]:
    registry = RuleRegistry()
    validator = RuleValidator()
    store = _InMemoryRuleStore()
    audit_store = _InMemoryAuditStore()
    event_bus = EventBus()
    service = RuleService(
        registry=registry,
        validator=validator,
        store=store,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )
    return service, audit_store


class TestRuleDefinition:
    def test_define_valid_rule(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        result = service.define(rule)
        assert result.rule_id == "qualification-budget"
        assert result.name == "Qualification Budget"

    def test_define_invalid_rule_missing_id(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule(rule_id="")
        with pytest.raises(Exception, match="rule_id is required"):
            service.define(rule)

    def test_define_invalid_rule_missing_name(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule(name="")
        with pytest.raises(Exception, match="name is required"):
            service.define(rule)

    def test_get_rule(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        result = service.get("qualification-budget")
        assert result.rule_id == "qualification-budget"

    def test_get_missing_rule_raises(self) -> None:
        service, _ = _make_service()
        with pytest.raises(RuleNotFoundError):
            service.get("nonexistent")

    def test_list_rules(self) -> None:
        service, _ = _make_service()
        service.define(_valid_rule(rule_id="r1", name="R1"))
        service.define(_valid_rule(rule_id="r2", name="R2"))
        results = service.list()
        assert len(results) == 2

    def test_validate_valid_rule(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        result = service.validate("qualification-budget")
        assert result.valid is True

    def test_validate_rule_with_warnings(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule(conditions=[])
        service.define(rule)
        result = service.validate("qualification-budget")
        assert result.valid is True
        assert any("no conditions" in w for w in result.warnings)


class TestValidator:
    def test_duplicate_condition_id(self) -> None:
        validator = RuleValidator()
        rule = _valid_rule(
            conditions=[
                RuleCondition(condition_id="c1", type="exists", field="f1"),
                RuleCondition(condition_id="c1", type="missing", field="f2"),
            ]
        )
        result = validator.validate(rule)
        assert not result.valid
        assert any("duplicate condition_id" in e for e in result.errors)

    def test_duplicate_action_id(self) -> None:
        validator = RuleValidator()
        rule = _valid_rule(
            actions=[
                RuleAction(action_id="a1", type="allow"),
                RuleAction(action_id="a1", type="deny"),
            ]
        )
        result = validator.validate(rule)
        assert not result.valid
        assert any("duplicate action_id" in e for e in result.errors)

    def test_unknown_condition_type(self) -> None:
        validator = RuleValidator()
        rule = _valid_rule(
            conditions=[
                RuleCondition.model_construct(condition_id="c1", type="invalid_type", field="f1"),
            ]
        )
        result = validator.validate(rule)
        assert not result.valid

    def test_unknown_action_type(self) -> None:
        validator = RuleValidator()
        rule = _valid_rule(
            actions=[
                RuleAction.model_construct(action_id="a1", type="invalid_action"),
            ]
        )
        result = validator.validate(rule)
        assert not result.valid

    def test_no_actions_warning(self) -> None:
        validator = RuleValidator()
        rule = _valid_rule(actions=[])
        result = validator.validate(rule)
        assert result.valid
        assert any("no actions defined" in w for w in result.warnings)


class TestEvaluation:
    def test_all_conditions_met(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        ctx = ExecutionContext(
            variables={
                "budget_known": True,
                "decision_maker_identified": True,
            }
        )
        result = service.evaluate(context=ctx)
        assert "qualification-budget" in result.matched_rules
        assert result.total_score_delta == 10.0

    def test_condition_not_met(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        ctx = ExecutionContext(
            variables={
                "budget_known": True,
                "decision_maker_identified": False,
            }
        )
        result = service.evaluate(context=ctx)
        assert "qualification-budget" in result.failed_rules
        assert result.total_score_delta == 0.0

    def test_equals_condition(self) -> None:
        rules = [
            _valid_rule(
                conditions=[
                    RuleCondition(condition_id="c1", type="equals", field="status", value="active"),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=5.0)],
            )
        ]
        ctx = ExecutionContext(variables={"status": "active"})
        result = evaluate_rules(rules, ctx)
        assert result.matched_rules == ["qualification-budget"]
        assert result.total_score_delta == 5.0

    def test_not_equals_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(
                        condition_id="c1", type="not_equals", field="status", value="inactive"
                    ),
                ],
                actions=[RuleAction(action_id="a1", type="deny")],
            )
        ]
        ctx = ExecutionContext(variables={"status": "active"})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules
        assert result.blocked is True

    def test_exists_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="email"),
                ],
                actions=[RuleAction(action_id="a1", type="allow")],
            )
        ]
        ctx = ExecutionContext(variables={"email": "test@example.com"})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules

    def test_missing_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="missing", field="email"),
                ],
                actions=[RuleAction(action_id="a1", type="allow")],
            )
        ]
        ctx = ExecutionContext(variables={})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules

    def test_greater_than_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="greater_than", field="score", value=50),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=10)],
            )
        ]
        ctx = ExecutionContext(variables={"score": 75})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules
        assert result.total_score_delta == 10.0

    def test_lower_than_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="lower_than", field="score", value=100),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=5)],
            )
        ]
        ctx = ExecutionContext(variables={"score": 75})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules

    def test_contains_condition(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="contains", field="tags", value="urgent"),
                ],
                actions=[RuleAction(action_id="a1", type="allow")],
            )
        ]
        ctx = ExecutionContext(variables={"tags": ["urgent", "important"]})
        result = evaluate_rules(rules, ctx)
        assert "test-rule" in result.matched_rules

    def test_set_variable_action(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="user"),
                ],
                actions=[
                    RuleAction(action_id="a1", type="set_variable", target="qualified", value=True),
                ],
            )
        ]
        ctx = ExecutionContext(variables={"user": "u1"})
        result = evaluate_rules(rules, ctx)
        assert result.variables.get("qualified") is True

    def test_emit_event_action(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="user"),
                ],
                actions=[
                    RuleAction(action_id="a1", type="emit_event", value="user.qualified"),
                ],
            )
        ]
        ctx = ExecutionContext(variables={"user": "u1"})
        result = evaluate_rules(rules, ctx)
        assert "user.qualified" in result.events

    def test_block_transition_action(self) -> None:
        rules = [
            _valid_rule(
                rule_id="test-rule",
                name="Test Rule",
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="blocked"),
                ],
                actions=[
                    RuleAction(action_id="a1", type="block_transition"),
                ],
            )
        ]
        ctx = ExecutionContext(variables={"blocked": True})
        result = evaluate_rules(rules, ctx)
        assert result.blocked is True

    def test_priority_ordering(self) -> None:
        rules = [
            _valid_rule(
                rule_id="high-priority",
                name="High",
                priority=200,
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="active"),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=20)],
            ),
            _valid_rule(
                rule_id="low-priority",
                name="Low",
                priority=50,
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="active"),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=5)],
            ),
        ]
        ctx = ExecutionContext(variables={"active": True})
        result = evaluate_rules(rules, ctx)
        assert "high-priority" in result.matched_rules
        assert "low-priority" in result.matched_rules
        assert result.total_score_delta == 25.0

    def test_disabled_rule_skipped(self) -> None:
        rules = [
            _valid_rule(
                rule_id="enabled-rule",
                name="Enabled",
                enabled=True,
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="active"),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=10)],
            ),
            _valid_rule(
                rule_id="disabled-rule",
                name="Disabled",
                enabled=False,
                conditions=[
                    RuleCondition(condition_id="c1", type="exists", field="active"),
                ],
                actions=[RuleAction(action_id="a1", type="add_score", value=20)],
            ),
        ]
        ctx = ExecutionContext(variables={"active": True})
        result = evaluate_rules(rules, ctx)
        assert "enabled-rule" in result.matched_rules
        assert "disabled-rule" not in result.matched_rules
        assert result.total_score_delta == 10.0

    def test_selective_evaluation(self) -> None:
        service, _ = _make_service()
        service.define(_valid_rule(rule_id="r1", name="R1"))
        service.define(_valid_rule(rule_id="r2", name="R2"))
        ctx = ExecutionContext(variables={"budget_known": True, "decision_maker_identified": True})
        result = service.evaluate(rules=["r1"], context=ctx)
        assert "r1" in result.matched_rules
        assert "r2" not in result.matched_rules


class TestExplain:
    def test_explain_matched_rule(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        ctx = ExecutionContext(
            variables={
                "budget_known": True,
                "decision_maker_identified": True,
            }
        )
        result = service.explain(context=ctx)
        assert len(result.entries) == 1
        entry = result.entries[0]
        assert entry.rule_id == "qualification-budget"
        assert entry.matched is True
        assert len(entry.conditions) == 2
        assert len(entry.actions) == 2

    def test_explain_failed_rule(self) -> None:
        service, _ = _make_service()
        rule = _valid_rule()
        service.define(rule)
        ctx = ExecutionContext(
            variables={
                "budget_known": True,
                "decision_maker_identified": False,
            }
        )
        result = service.explain(context=ctx)
        assert len(result.entries) == 1
        entry = result.entries[0]
        assert entry.matched is False

    def test_explain_selective_rules(self) -> None:
        service, _ = _make_service()
        service.define(_valid_rule(rule_id="r1", name="R1"))
        service.define(_valid_rule(rule_id="r2", name="R2"))
        ctx = ExecutionContext(variables={})
        result = service.explain(rules=["r1"], context=ctx)
        assert len(result.entries) == 1
        assert result.entries[0].rule_id == "r1"


class TestSerialization:
    def test_rule_definition_roundtrip(self) -> None:
        rule = _valid_rule()
        serialized = rule.model_dump()
        restored = RuleDefinition.model_validate(serialized)
        assert restored.rule_id == rule.rule_id
        assert restored.model_dump() == serialized
