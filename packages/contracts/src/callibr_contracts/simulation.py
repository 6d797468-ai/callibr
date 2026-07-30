from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from callibr_contracts.crm import CrmActionExecution

ScenarioLevel = Literal["foundation", "intermediate", "advanced"]
ScenarioChannel = Literal["chat", "voice", "email", "backoffice"]
SimulationStatus = Literal["active", "completed"]
MessageRole = Literal["learner", "customer", "system", "coach"]
EvaluationCriterionStatus = Literal["passed", "missed"]


class ReplayTurn(BaseModel):
    turn_index: int = Field(ge=0)
    learner_message: str
    customer_message: str
    evaluation: SimulationEvaluation | None = None


class SessionReplay(BaseModel):
    session_id: str
    tenant_id: str
    learner_id: str
    scenario: ScenarioSummary
    started_at: datetime
    completed_at: datetime | None = None
    status: SimulationStatus
    turns: list[ReplayTurn] = Field(default_factory=list)


class ScenarioSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    scenario_id: str
    domain_pack: str
    title: str
    level: ScenarioLevel
    channel: ScenarioChannel
    estimated_minutes: int = Field(ge=1)
    learning_goals: list[str] = Field(default_factory=list)


class SimulationMessage(BaseModel):
    role: MessageRole
    content: str = Field(min_length=1)
    at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationCriterionResult(BaseModel):
    criterion_id: str
    label: str
    status: EvaluationCriterionStatus
    score: int = Field(ge=0)
    max_score: int = Field(default=20, ge=1)
    evidence: list[str] = Field(default_factory=list)
    feedback: str


class SimulationEvaluation(BaseModel):
    score: int = Field(ge=0, le=100)
    max_score: int = 100
    criteria: list[EvaluationCriterionResult] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_best_actions: list[str] = Field(default_factory=list)


class SimulationSession(BaseModel):
    session_id: str
    tenant_id: str
    learner_id: str
    scenario: ScenarioSummary
    status: SimulationStatus
    current_step: str
    started_at: datetime
    completed_at: datetime | None = None
    messages: list[SimulationMessage] = Field(default_factory=list)
    crm_context: dict[str, Any] = Field(default_factory=dict)
    crm_actions: list[CrmActionExecution] = Field(default_factory=list)
    evaluation: SimulationEvaluation | None = None
    customer_profile: dict[str, Any] | None = None
    # Bridge fields -- populated when ConversationService is active
    conversation_session_id: str | None = None
    procedure_execution_id: str | None = None


class StartSimulationRequest(BaseModel):
    tenant_id: str = Field(default="tenant_demo", min_length=1)
    learner_id: str = Field(default="learner_demo", min_length=1)
    scenario_id: str = Field(min_length=1)


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class SendMessageResponse(BaseModel):
    session: SimulationSession
    customer_message: SimulationMessage
    evaluation: SimulationEvaluation


class SessionReport(BaseModel):
    session_id: str
    tenant_id: str
    learner_id: str
    scenario: ScenarioSummary
    status: SimulationStatus
    generated_at: datetime
    started_at: datetime
    completed_at: datetime | None = None
    duration_seconds: int = Field(ge=0)
    message_count: int = Field(ge=0)
    learner_message_count: int = Field(ge=0)
    customer_message_count: int = Field(ge=0)
    crm_action_count: int = Field(ge=0)
    audit_event_count: int = Field(ge=0)
    final_score: int = Field(ge=0, le=100)
    max_score: int = Field(default=100, ge=1)
    criteria: list[EvaluationCriterionResult] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_best_actions: list[str] = Field(default_factory=list)
    crm_actions: list[CrmActionExecution] = Field(default_factory=list)
    # Procedural progress -- populated when bridge is active
    procedure_execution_id: str | None = None
    procedure_progress: list[dict[str, Any]] = Field(default_factory=list)
