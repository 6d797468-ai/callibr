from __future__ import annotations

from callibr_kernel import CallibrError


class TokenBudgetExceededError(CallibrError):
    def __init__(
        self,
        *,
        available_tokens: int,
        required_tokens: int,
    ) -> None:
        self.available_tokens = available_tokens
        self.required_tokens = required_tokens

        super().__init__(
            code="token_budget_exceeded",
            message="The conversation context exceeds the available token budget.",
            details={
                "available_tokens": available_tokens,
                "required_tokens": required_tokens,
            },
        )


class LLMError(CallibrError):
    def __init__(
        self,
        message: str,
        *,
        details: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            code="llm_error",
            message=message,
            details=details or {},
        )


class AdapterError(LLMError):
    def __init__(
        self,
        provider: str,
        model: str,
        original_error: str,
    ) -> None:
        self.provider = provider
        self.model = model
        super().__init__(
            message=f"LLM adapter '{provider}/{model}' failed: {original_error}",
            details={
                "provider": provider,
                "model": model,
                "original_error": original_error,
            },
        )


class ProviderNotAvailableError(LLMError):
    def __init__(self, provider: str, model: str) -> None:
        self.provider = provider
        self.model = model
        super().__init__(
            message=f"Provider '{provider}' is not available for model '{model}'.",
            details={"provider": provider, "model": model},
        )


class ModelNotFoundError(LLMError):
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(
            message=f"Model '{model_id}' is not registered in any provider.",
            details={"model_id": model_id},
        )


class SafetyViolationError(LLMError):
    def __init__(
        self,
        *,
        direction: str,
        reason: str,
        categories: list[str] | None = None,
    ) -> None:
        super().__init__(
            message=f"Safety violation ({direction}): {reason}",
            details={
                "direction": direction,
                "reason": reason,
                "categories": categories or [],
            },
        )
