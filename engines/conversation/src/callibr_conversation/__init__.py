"""Conversation Runtime — Orchestrator pipeline for Callibr."""

from callibr_conversation.adapters import MockAdapter, OpenAIAdapter  # type: ignore[attr-defined]
from callibr_conversation.adapters.ollama import OllamaAdapter
from callibr_conversation.budget import TokenBudgetEvaluator
from callibr_conversation.errors import (
    AdapterError,
    LLMError,
    ModelNotFoundError,
    ProviderNotAvailableError,
    SafetyViolationError,
    TokenBudgetExceededError,
)
from callibr_conversation.events import ConversationEvent
from callibr_conversation.memory import SessionMemory, TurnMemory
from callibr_conversation.orchestrator import ContextBuilder
from callibr_conversation.reducer import PriorityContextReducer
from callibr_conversation.router import CapabilityBasedRouter, ProviderRegistry
from callibr_conversation.safety import DeterministicSafetyValidator
from callibr_conversation.service import (
    ConversationService,
    SessionNotFoundError,
)
from callibr_conversation.token_counter import DeterministicTokenCounter

__all__ = [
    "AdapterError",
    "CapabilityBasedRouter",
    "ContextBuilder",
    "ConversationEvent",
    "ConversationService",
    "DeterministicSafetyValidator",
    "DeterministicTokenCounter",
    "LLMError",
    "MockAdapter",
    "ModelNotFoundError",
    "OllamaAdapter",
    "OpenAIAdapter",
    "PriorityContextReducer",
    "ProviderNotAvailableError",
    "ProviderRegistry",
    "SafetyViolationError",
    "SessionMemory",
    "SessionNotFoundError",
    "TokenBudgetEvaluator",
    "TokenBudgetExceededError",
    "TurnMemory",
]
