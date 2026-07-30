from __future__ import annotations

import logging

from callibr_contracts import (
    LLMAdapter,
    ModelCapability,
    ModelRequest,
    ModelRequirements,
)

from callibr_conversation.errors import ModelNotFoundError, ProviderNotAvailableError

log = logging.getLogger(__name__)


class ProviderRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, LLMAdapter] = {}
        self._capabilities: dict[str, set[ModelCapability]] = {}
        self._context_windows: dict[str, int] = {}

    def register(
        self,
        model_id: str,
        adapter: LLMAdapter,
        capabilities: set[ModelCapability] | None = None,
        context_window: int | None = None,
    ) -> None:
        self._adapters[model_id] = adapter
        self._capabilities[model_id] = capabilities or {ModelCapability.CHAT}
        if context_window is not None:
            self._context_windows[model_id] = context_window

    def unregister(self, model_id: str) -> None:
        self._adapters.pop(model_id, None)
        self._capabilities.pop(model_id, None)
        self._context_windows.pop(model_id, None)

    def get_adapter(self, model_id: str) -> LLMAdapter | None:
        return self._adapters.get(model_id)

    def list_models(self) -> list[str]:
        return list(self._adapters.keys())


class CapabilityBasedRouter:
    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def select(self, request: ModelRequest) -> LLMAdapter:
        model_id = self._find_best_match(request.requirements)
        adapter = self._registry.get_adapter(model_id)
        if adapter is None:
            raise ProviderNotAvailableError(
                provider="unknown",
                model=model_id,
            )
        log.info(
            "Router selected model='%s' for request with capabilities=%s",
            model_id,
            request.requirements.required_capabilities,
        )
        return adapter

    def _find_best_match(self, requirements: ModelRequirements) -> str:
        if requirements.preferred_model:
            adapter = self._registry.get_adapter(requirements.preferred_model)
            if adapter is not None:
                return requirements.preferred_model

        candidates: list[tuple[int, str]] = []
        for model_id in self._registry.list_models():
            caps = self._registry._capabilities.get(model_id, set())
            if requirements.required_capabilities - caps:
                continue

            cw = self._registry._context_windows.get(model_id, 0)
            if requirements.min_context_window and cw < requirements.min_context_window:
                continue

            candidates.append((cw, model_id))

        if not candidates:
            raise ModelNotFoundError(str(requirements.required_capabilities))

        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]
