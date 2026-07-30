"""Rule Engine — Declarative business rules for Callibr."""

from callibr_rule.evaluator import evaluate_rules, explain_rules
from callibr_rule.events import RuleEvent
from callibr_rule.registry import RuleRegistry
from callibr_rule.service import RuleNotFoundError, RuleService
from callibr_rule.validators import RuleValidator

__all__ = [
    "evaluate_rules",
    "explain_rules",
    "RuleEvent",
    "RuleNotFoundError",
    "RuleRegistry",
    "RuleService",
    "RuleValidator",
]
