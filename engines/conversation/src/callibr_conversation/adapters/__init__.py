"""LLM adapters — MockAdapter for deterministic testing."""

from __future__ import annotations

import logging
from typing import Any

import openai
from callibr_contracts import ModelRequest, ModelResponse

from callibr_conversation.errors import AdapterError

log = logging.getLogger(__name__)


class MockAdapter:
    def __init__(self, response_text: str = "Ceci est une réponse simulée.") -> None:
        self._response_text = response_text
        self._call_count = 0
        self._last_request: ModelRequest | None = None

    def generate(self, request: ModelRequest) -> ModelResponse:
        self._call_count += 1
        self._last_request = request
        return ModelResponse(
            content=self._response_text,
            model_id="mock",
            finish_reason="stop",
            usage={"prompt_tokens": 0, "completion_tokens": 0},
        )

    def stream(self, request: ModelRequest) -> ...:
        yield ModelResponse(
            content=self._response_text,
            model_id="mock",
            finish_reason="stop",
        )

    def health(self) -> bool:
        return True

    def metadata(self) -> dict[str, Any]:
        return {"model_id": "mock", "provider": "mock"}

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def last_request(self) -> ModelRequest | None:
        return self._last_request


class OpenAIAdapter:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._api_key = api_key
        self._model = model
        self._client = openai.OpenAI(api_key=api_key)
        self._call_count = 0
        self._last_request: ModelRequest | None = None

    def generate(self, request: ModelRequest) -> ModelResponse:
        self._call_count += 1
        self._last_request = request

        system_message = {"role": "system", "content": request.system_prompt}
        messages = [system_message, *request.messages]

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,  # type: ignore[arg-type]
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            from callibr_telemetry import llm_tokens_total

            prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
            completion_tokens = getattr(response.usage, "completion_tokens", 0)

            if prompt_tokens > 0:
                llm_tokens_total.labels(model=self._model, token_type="prompt").inc(prompt_tokens)
            if completion_tokens > 0:
                llm_tokens_total.labels(model=self._model, token_type="completion").inc(
                    completion_tokens
                )

            choice = response.choices[0]
            content = choice.message.content or ""
            finish_reason = choice.finish_reason or "stop"

            usage_dict = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }

            return ModelResponse(
                content=content,
                model_id=self._model,
                finish_reason=finish_reason,
                usage=usage_dict,
            )
        except openai.OpenAIError as exc:
            log.error("OpenAI generation failed: %s", exc)
            raise AdapterError(
                provider="openai",
                model=self._model,
                original_error=str(exc),
            ) from exc

    def stream(self, request: ModelRequest) -> ...:
        raise NotImplementedError("Streaming is not yet implemented for OpenAIAdapter.")

    def health(self) -> bool:
        try:
            # A simple lightweight call to verify authentication
            self._client.models.list()
            return True
        except Exception:
            return False

    def metadata(self) -> dict[str, Any]:
        return {"model_id": self._model, "provider": "openai"}

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def last_request(self) -> ModelRequest | None:
        return self._last_request
