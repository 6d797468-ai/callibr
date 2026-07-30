from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ConversationStage(StrEnum):
    opening = "opening"
    discovery = "discovery"
    handling = "handling"
    objection = "objection"
    closing = "closing"
    evaluation = "evaluation"
    completed = "completed"


class DirectorCommand(StrEnum):
    speak = "speak"
    listen = "listen"
    change_subject = "change_subject"
    introduce_objection = "introduce_objection"
    increase_difficulty = "increase_difficulty"
    decrease_difficulty = "decrease_difficulty"
    stay_silent = "stay_silent"
    ask_for_details = "ask_for_details"
    provide_hint = "provide_hint"
    congratulate = "congratulate"
    conclude_turn = "conclude_turn"
    end_session = "end_session"


class DirectorDecision(BaseModel):
    command: DirectorCommand
    next_stage: ConversationStage
    reason: str = ""
    difficulty_delta: int = 0
    wait_for_learner: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class DirectorContext(BaseModel):
    session_id: str
    tenant_id: str
    scenario_id: str
    persona_id: str
    stage: ConversationStage = ConversationStage.opening
    turn_count: int = 0
    learner_message_count: int = 0
    current_score: int = 0
    max_score: int = 100
    last_intent: str = ""
    last_learner_emotion: str = "neutral"
    stage_duration_seconds: float = 0.0
    total_duration_seconds: float = 0.0
    procedure_step_id: str = ""
    scenario_difficulty: str = "foundation"
    rules_triggered: list[str] = Field(default_factory=list)
