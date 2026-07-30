from __future__ import annotations

from typing import Annotated, Any

from callibr_api.dependencies import get_conversation_service
from callibr_contracts import ConversationResult, ConversationState
from callibr_conversation import ConversationService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/conversations", tags=["Conversation Runtime"])


@router.post("", status_code=201)
def start_conversation(
    scenario_id: str,
    service: Annotated[ConversationService, Depends(get_conversation_service)],
    tenant_id: str = "tenant_demo",
    actor_id: str = "learner_demo",
    extra_context: dict[str, Any] | None = None,
) -> ConversationResult:
    return service.start_conversation(scenario_id, tenant_id, actor_id, extra_context)


@router.post("/{session_id}/messages")
def process_message(
    session_id: str,
    service: Annotated[ConversationService, Depends(get_conversation_service)],
    message: str,
) -> ConversationResult:
    return service.process_message(session_id, message)


@router.get("/{session_id}")
def get_session_state(
    session_id: str,
    service: Annotated[ConversationService, Depends(get_conversation_service)],
) -> ConversationState:
    return service.get_session_state(session_id)
