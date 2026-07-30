from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CommunicationIntent(StrEnum):
    reassure_customer = "reassure_customer"
    explain_delay = "explain_delay"
    apologize = "apologize"
    ask_for_info = "ask_for_info"
    propose_solution = "propose_solution"
    confirm_understanding = "confirm_understanding"
    escalate = "escalate"
    close_conversation = "close_conversation"
    probe_for_details = "probe_for_details"
    handle_objection = "handle_objection"
    give_instruction = "give_instruction"
    acknowledge = "acknowledge"
    summarize = "summarize"
    redirect = "redirect"
    stay_silent = "stay_silent"
    congratulate = "congratulate"
    challenge_learner = "challenge_learner"
    create_urgency = "create_urgency"
    de_escalate = "de_escalate"


class CommunicationGoal(StrEnum):
    explain = "explain"
    apologize = "apologize"
    reassure = "reassure"
    gather_info = "gather_info"
    propose = "propose"
    confirm = "confirm"
    instruct = "instruct"
    probe = "probe"
    object = "object"
    conclude = "conclude"
    praise = "praise"
    challenge = "challenge"


class ResponseTone(StrEnum):
    calm = "calm"
    empathetic = "empathetic"
    professional = "professional"
    warm = "warm"
    firm = "firm"
    urgent = "urgent"
    friendly = "friendly"
    neutral = "neutral"


class VoiceStyle(StrEnum):
    warm = "warm"
    professional = "professional"
    friendly = "friendly"
    calm = "calm"
    neutral = "neutral"


class ResponseConstraint(BaseModel):
    max_sentences: int = Field(default=3, ge=1, le=6)
    min_sentences: int = Field(default=1, ge=1)
    language: str = "fr"
    no_technical_terms: bool = False
    empathetic: bool = False
    must_include: list[str] = Field(default_factory=list)
    must_avoid: list[str] = Field(default_factory=list)


class ResponsePlan(BaseModel):
    intent: CommunicationIntent
    goals: list[CommunicationGoal] = Field(min_length=1)
    constraints: ResponseConstraint = Field(default_factory=ResponseConstraint)
    tone: ResponseTone = ResponseTone.professional
    voice: VoiceStyle = VoiceStyle.professional
    expected_outcome: str = ""
    context_variables: dict[str, Any] = Field(default_factory=dict)
    procedure_step_id: str = ""


class PlanningContext(BaseModel):
    scenario_id: str
    persona_id: str
    procedure_id: str
    procedure_step_id: str
    current_stage: str
    learner_message: str = ""
    last_customer_message: str = ""
    evaluation_score: int = 0
    turn_count: int = 0
    crm_context: dict[str, Any] = Field(default_factory=dict)
    rule_matches: list[str] = Field(default_factory=list)
    detected_emotion: str = "neutral"
    session_duration_seconds: float = 0.0
