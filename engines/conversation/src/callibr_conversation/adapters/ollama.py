from __future__ import annotations

import logging
from typing import Any

import httpx
from callibr_contracts import ModelRequest, ModelResponse

from callibr_conversation.errors import AdapterError

log = logging.getLogger(__name__)

DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2"


class OllamaAdapter:
    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        model: str = DEFAULT_OLLAMA_MODEL,
        timeout: float = 60.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout)
        self._call_count = 0
        self._last_request: ModelRequest | None = None

    def generate(self, request: ModelRequest) -> ModelResponse:
        self._call_count += 1
        self._last_request = request

        messages: list[dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.extend(request.messages)

        try:
            response = self._client.post(
                "/api/chat",
                json={
                    "model": self._model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens,
                    },
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        except httpx.HTTPStatusError as exc:
            raise AdapterError(
                provider="ollama",
                model=self._model,
                original_error=f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
            ) from exc
        except httpx.RequestError as exc:
            raise AdapterError(
                provider="ollama",
                model=self._model,
                original_error=str(exc),
            ) from exc

        content = data.get("message", {}).get("content", "")
        usage: dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0}

        return ModelResponse(
            content=content,
            model_id=self._model,
            finish_reason="stop",
            usage=usage,
        )

    def stream(self, request: ModelRequest) -> ...:
        raise NotImplementedError("Streaming is not yet implemented for OllamaAdapter.")

    def health(self) -> bool:
        try:
            resp = self._client.get("/api/tags")
            return resp.status_code == 200
        except Exception:
            return False

    def metadata(self) -> dict[str, Any]:
        return {"provider": "ollama", "model_id": self._model, "base_url": self._base_url}

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def last_request(self) -> ModelRequest | None:
        return self._last_request
