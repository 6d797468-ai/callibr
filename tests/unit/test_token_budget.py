from __future__ import annotations

import pytest
from callibr_contracts import ModelRequest, TokenBudget, TokenBudgetResult, TokenUsage
from callibr_conversation import (
    DeterministicTokenCounter,
    TokenBudgetEvaluator,
    TokenBudgetExceededError,
)
from pydantic import ValidationError


class TestTokenBudget:
    def test_available_input_tokens_is_calculated_correctly(self) -> None:
        budget = TokenBudget(context_window=8_192, reserved_output_tokens=1_024, safety_margin_tokens=256)
        assert budget.available_input_tokens == 8_192 - 1_024 - 256

    def test_budget_rejects_when_reserved_exceeds_window(self) -> None:
        with pytest.raises(ValidationError):
            TokenBudget(context_window=1_000, reserved_output_tokens=800, safety_margin_tokens=300)

    def test_budget_rejects_when_reserved_equals_window(self) -> None:
        with pytest.raises(ValidationError):
            TokenBudget(context_window=1_000, reserved_output_tokens=1_000, safety_margin_tokens=0)

    def test_budget_rejects_zero_context_window(self) -> None:
        with pytest.raises(ValidationError):
            TokenBudget(context_window=0, reserved_output_tokens=0, safety_margin_tokens=0)

    def test_budget_is_immutable(self) -> None:
        budget = TokenBudget(context_window=8_192, reserved_output_tokens=1_024, safety_margin_tokens=256)
        with pytest.raises(ValidationError):
            budget.context_window = 999


class TestTokenUsage:
    def test_usage_is_immutable(self) -> None:
        usage = TokenUsage(system_tokens=10, conversation_tokens=20, context_tokens=5, total_input_tokens=35)
        with pytest.raises(ValidationError):
            usage.system_tokens = 99

    def test_rejects_inconsistent_total(self) -> None:
        with pytest.raises(ValidationError):
            TokenUsage(system_tokens=10, conversation_tokens=20, context_tokens=5, total_input_tokens=999)

    def test_accepts_consistent_total(self) -> None:
        usage = TokenUsage(system_tokens=10, conversation_tokens=20, context_tokens=5, total_input_tokens=35)
        assert usage.total_input_tokens == 35


class TestDeterministicTokenCounter:
    def test_same_request_produces_same_count(self) -> None:
        counter = DeterministicTokenCounter()
        req = ModelRequest(system_prompt="Hello", messages=[{"role": "user", "content": "Hi"}])
        u1 = counter.count(req)
        u2 = counter.count(req)
        assert u1 == u2

    def test_empty_content_returns_zero(self) -> None:
        counter = DeterministicTokenCounter()
        req = ModelRequest()
        usage = counter.count(req)
        assert usage.system_tokens == 0
        assert usage.conversation_tokens == 0
        assert usage.context_tokens == 0
        assert usage.total_input_tokens == 0

    def test_non_empty_short_text_counts_at_least_one_token(self) -> None:
        counter = DeterministicTokenCounter()
        req = ModelRequest(system_prompt="A")
        usage = counter.count(req)
        assert usage.system_tokens >= 1

    def test_message_overhead_is_applied(self) -> None:
        counter = DeterministicTokenCounter()
        req = ModelRequest(messages=[{"role": "user", "content": ""}])
        usage = counter.count(req)
        assert usage.context_tokens > 0

    def test_sections_are_counted_separately(self) -> None:
        counter = DeterministicTokenCounter(characters_per_token=4, message_overhead=4)
        req = ModelRequest(
            system_prompt="Hello world",
            system_context="System context",
            messages=[{"role": "user", "content": "User message"}],
            persona_context="Persona",
            scenario_context="Scenario",
            procedure_context="Procedure",
            rule_context="Rule",
            crm_context="CRM",
            memory_context="Memory",
        )
        usage = counter.count(req)
        assert usage.system_tokens > 0
        assert usage.conversation_tokens > 0
        assert usage.context_tokens > 0
        assert usage.total_input_tokens == usage.system_tokens + usage.conversation_tokens + usage.context_tokens

    def test_does_not_import_external_tokenizer(self) -> None:
        import sys
        modules = [m for m in sys.modules if "tiktoken" in m]
        assert len(modules) == 0

    def test_default_characters_per_token(self) -> None:
        counter = DeterministicTokenCounter()
        assert counter._characters_per_token == 4

    def test_rejects_invalid_characters_per_token(self) -> None:
        with pytest.raises(ValueError, match="characters_per_token must be positive"):
            DeterministicTokenCounter(characters_per_token=0)

    def test_rejects_negative_message_overhead(self) -> None:
        with pytest.raises(ValueError, match="message_overhead cannot be negative"):
            DeterministicTokenCounter(message_overhead=-1)


class TestTokenBudgetEvaluator:
    def test_context_exactly_at_budget_is_accepted(self) -> None:
        counter = DeterministicTokenCounter(characters_per_token=100, message_overhead=0)
        evaluator = TokenBudgetEvaluator(counter)
        budget = TokenBudget(context_window=1_000, reserved_output_tokens=0, safety_margin_tokens=0)
        req = ModelRequest(system_prompt="x" * 100)
        result = evaluator.evaluate(req, budget)
        assert result.within_budget
        assert result.overflow_tokens == 0

    def test_overflow_by_one_token_is_detected(self) -> None:
        counter = DeterministicTokenCounter(characters_per_token=100, message_overhead=0)
        evaluator = TokenBudgetEvaluator(counter)
        budget = TokenBudget(context_window=1, reserved_output_tokens=0, safety_margin_tokens=0)
        req = ModelRequest(system_prompt="x" * 101)
        result = evaluator.evaluate(req, budget)
        assert not result.within_budget
        assert result.overflow_tokens >= 1


class TestTokenBudgetResult:
    def test_result_is_immutable(self) -> None:
        budget = TokenBudget(context_window=8_192, reserved_output_tokens=1_024, safety_margin_tokens=256)
        usage = TokenUsage(system_tokens=10, conversation_tokens=20, context_tokens=5, total_input_tokens=35)
        result = TokenBudgetResult(budget=budget, usage=usage, within_budget=True, overflow_tokens=0)
        with pytest.raises(ValidationError):
            result.within_budget = False


class TestTokenBudgetExceededError:
    def test_error_has_correct_code(self) -> None:
        err = TokenBudgetExceededError(available_tokens=1_000, required_tokens=1_200)
        assert err.code == "token_budget_exceeded"

    def test_error_inherits_from_callibr_error(self) -> None:
        from callibr_kernel import CallibrError
        err = TokenBudgetExceededError(available_tokens=1_000, required_tokens=1_200)
        assert isinstance(err, CallibrError)

    def test_error_exposes_numbers_in_details(self) -> None:
        err = TokenBudgetExceededError(available_tokens=1_000, required_tokens=1_200)
        assert err.details["available_tokens"] == 1_000
        assert err.details["required_tokens"] == 1_200


class TestModelRequestImmutability:
    def test_original_request_is_not_modified_by_counter(self) -> None:
        counter = DeterministicTokenCounter()
        req = ModelRequest(system_prompt="Hello", messages=[{"role": "user", "content": "World"}])
        original_system = req.system_prompt
        original_msgs = list(req.messages)
        counter.count(req)
        assert req.system_prompt == original_system
        assert req.messages == original_msgs

    def test_model_request_is_immutable(self) -> None:
        req = ModelRequest(system_prompt="Hello")
        with pytest.raises(ValidationError):
            req.system_prompt = "Changed"
