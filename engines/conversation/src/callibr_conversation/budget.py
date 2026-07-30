from __future__ import annotations

from callibr_contracts import ModelRequest, TokenBudget, TokenBudgetResult, TokenCounter


class TokenBudgetEvaluator:
    def __init__(self, counter: TokenCounter) -> None:
        self._counter = counter

    def evaluate(
        self,
        request: ModelRequest,
        budget: TokenBudget,
    ) -> TokenBudgetResult:
        usage = self._counter.count(request)

        return TokenBudgetResult(
            budget=budget,
            usage=usage,
            within_budget=(
                usage.total_input_tokens
                <= budget.available_input_tokens
            ),
            overflow_tokens=max(
                0,
                usage.total_input_tokens
                - budget.available_input_tokens,
            ),
        )
