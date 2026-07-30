from __future__ import annotations

import logging
from typing import Any

from callibr_contracts import ConversationContext, TokenBudget

log = logging.getLogger(__name__)

NON_SUPPRESSIBLE_FIELDS = frozenset({
    "metadata",
    "conversation_state",
})

PRIORITY_ORDER = [
    "system_context",
    "persona_context",
    "procedure_context",
    "rule_context",
    "evaluation_context",
    "crm_context",
    "memory_context",
    "scenario_context",
]


class PriorityContextReducer:
    def reduce(
        self,
        context: ConversationContext,
        budget: TokenBudget,
    ) -> ConversationContext:
        estimated = self._estimate_tokens(context)
        available = budget.available_input_tokens

        if estimated <= available:
            return context

        log.info(
            "Context reduction needed: estimated=%d, available=%d",
            estimated,
            available,
        )

        current = context
        for field in reversed(PRIORITY_ORDER):
            if field in NON_SUPPRESSIBLE_FIELDS:
                continue

            value = getattr(current, field, None)
            if value is None or value == self._empty_for_type(value):
                continue

            cleared = self._clear_field(field, current)

            reduced_estimated = self._estimate_tokens(cleared)
            if reduced_estimated <= available:
                log.info("Reduced field '%s' to fit budget", field)
                return cleared

            current = cleared

        return current

    def _clear_field(
        self,
        field: str,
        context: ConversationContext,
    ) -> ConversationContext:
        values = {}
        for f in ConversationContext.model_fields:
            if f == field:
                val = getattr(context, f)
                values[f] = self._empty_for_type(val)
            else:
                values[f] = getattr(context, f)

        return ConversationContext(**values)

    def _empty_for_type(self, value: Any) -> Any:
        if isinstance(value, str):
            return ""
        if isinstance(value, dict):
            return {}
        if isinstance(value, list):
            return []
        return value

    def _estimate_tokens(self, context: ConversationContext) -> int:
        total = 0
        for field in PRIORITY_ORDER:
            val = getattr(context, field, None)
            if val is None:
                continue
            total += self._count(val)
        return total

    def _count(self, value: Any) -> int:
        if isinstance(value, str):
            return max(1, (len(value) + 3) // 4)
        if isinstance(value, dict):
            s = sum(self._count(v) for v in value.values())
            return s + len(value)
        if isinstance(value, list):
            s = sum(self._count(v) for v in value)
            return s + len(value)
        return 1
