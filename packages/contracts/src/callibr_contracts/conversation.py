from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Protocol
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from callibr_contracts.persona import PromptContext
from callibr_contracts.rule import RuleEvaluation


class ModelCapability(StrEnum):
    CHAT = "chat"
    STREAMING = "streaming"
    JSON_MODE = "json_mode"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"


class ModelRequirements(BaseModel):
    model_config = ConfigDict(frozen=True)

    required_capabilities: set[ModelCapability] = Field(
        default_factory=lambda: {ModelCapability.CHAT}
    )
    min_context_window: int | None = None
    preferred_model: str | None = None


class ConversationTurn(BaseModel):
    model_config = ConfigDict(frozen=True)

    turn_id: str
    role: str
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConversationState(BaseModel):
    model_config = ConfigDict(frozen=True)

    session_id: str
    correlation_id: UUID
    version: int = 0
    turns: list[ConversationTurn] = Field(default_factory=list)
    current_step_id: str = ""
    variables: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime
    updated_at: datetime


class ConversationStore(Protocol):
    def save(self, state: ConversationState, conn: Any = None) -> None: ...

    def get(self, session_id: str) -> ConversationState | None: ...


class ConversationMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenant_id: str = "tenant_demo"
    actor_id: str = "learner_demo"
    scenario_id: str = ""
    procedure_id: str = ""
    execution_id: str = ""
    persona_id: str = ""
    trace_id: str = ""


class ConversationContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    system_context: str = ""
    persona_context: PromptContext = Field(default_factory=PromptContext)
    scenario_context: dict[str, Any] = Field(default_factory=dict)
    procedure_context: dict[str, Any] = Field(default_factory=dict)
    rule_context: RuleEvaluation = Field(default_factory=lambda: RuleEvaluation(results=[]))
    crm_context: dict[str, Any] = Field(default_factory=dict)
    memory_context: dict[str, Any] = Field(default_factory=dict)
    evaluation_context: dict[str, Any] = Field(default_factory=dict)
    plan_context: str = ""
    metadata: ConversationMetadata = Field(default_factory=ConversationMetadata)
    conversation_state: ConversationState | None = None


class ModelResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    content: str
    model_id: str = "mock"
    finish_reason: str = "stop"
    usage: dict[str, int] = Field(
        default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0}
    )


class ModelRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    system_prompt: str = ""
    messages: list[dict[str, str]] = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 1024
    system_context: str = ""
    persona_context: str = ""
    scenario_context: str = ""
    procedure_context: str = ""
    rule_context: str = ""
    crm_context: str = ""
    memory_context: str = ""
    requirements: ModelRequirements = Field(default_factory=ModelRequirements)


class TokenBudget(BaseModel):
    model_config = ConfigDict(frozen=True)

    context_window: int = Field(gt=0)
    reserved_output_tokens: int = Field(ge=0)
    safety_margin_tokens: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_capacity(self) -> TokenBudget:
        reserved = self.reserved_output_tokens + self.safety_margin_tokens
        if reserved >= self.context_window:
            raise ValueError(
                "reserved_output_tokens + safety_margin_tokens "
                "must be lower than context_window"
            )
        return self

    @property
    def available_input_tokens(self) -> int:
        return (
            self.context_window
            - self.reserved_output_tokens
            - self.safety_margin_tokens
        )


class TokenUsage(BaseModel):
    model_config = ConfigDict(frozen=True)

    system_tokens: int = Field(ge=0)
    conversation_tokens: int = Field(ge=0)
    context_tokens: int = Field(ge=0)
    total_input_tokens: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_total(self) -> TokenUsage:
        calculated = (
            self.system_tokens
            + self.conversation_tokens
            + self.context_tokens
        )
        if self.total_input_tokens != calculated:
            raise ValueError(
                "total_input_tokens must equal the sum of token categories"
            )
        return self


class TokenBudgetResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    budget: TokenBudget
    usage: TokenUsage
    within_budget: bool
    overflow_tokens: int = Field(ge=0)


class TokenCounter(Protocol):
    def count(self, request: ModelRequest) -> TokenUsage: ...


class ContextReducer(Protocol):
    def reduce(self, context: ConversationContext, budget: TokenBudget) -> ConversationContext: ...


class SafetyResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    is_safe: bool
    reason: str | None = None
    flagged_categories: list[str] = Field(default_factory=list)


class SafetyValidator(Protocol):
    def validate_input(self, request: ModelRequest) -> SafetyResult: ...

    def validate_output(self, response: ModelResponse) -> SafetyResult: ...


class LLMAdapter(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse: ...

    def stream(self, request: ModelRequest) -> ...: ...

    def health(self) -> bool: ...

    def metadata(self) -> dict[str, Any]: ...


class LLMRouter(Protocol):
    def select(self, request: ModelRequest) -> LLMAdapter: ...


class ConversationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    context: ConversationContext
    response: ModelResponse
    state: ConversationState
