from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Annotated

from callibr_api.config import get_settings
from callibr_voice import (
    DeepgramSTTAdapter,
    ElevenLabsTTSAdapter,
    MockSTTAdapter,
    MockTTSAdapter,
    STTAdapter,
    TTSAdapter,
    VoiceSessionService,
    VoiceSessionState,
)
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/voice", tags=["Voice"])

_voice_service = VoiceSessionService()


def get_voice_service() -> VoiceSessionService:
    return _voice_service


VoiceServiceDep = Annotated[VoiceSessionService, Depends(get_voice_service)]


@lru_cache
def get_stt_adapter() -> STTAdapter:
    settings = get_settings()
    if settings.mock_stt:
        log.info("Voice: using Mock STT")
        return MockSTTAdapter()
    api_key = os.environ.get("DEEPGRAM_API_KEY", "")
    log.info("Voice: using Deepgram STT")
    return DeepgramSTTAdapter(api_key=api_key)


@lru_cache
def get_tts_adapter() -> TTSAdapter:
    settings = get_settings()
    if settings.mock_tts:
        log.info("Voice: using Mock TTS")
        return MockTTSAdapter()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    log.info("Voice: using ElevenLabs TTS")
    return ElevenLabsTTSAdapter(api_key=api_key, voice_id=voice_id)


@router.post("/sessions")
def create_voice_session(
    simulation_session_id: str,
    service: VoiceServiceDep,
) -> dict:
    session = service.create_session(simulation_session_id)
    return {
        "session_id": session.session_id,
        "state": session.state.value,
        "config": session.config.model_dump(),
    }


@router.get("/sessions/{session_id}")
def get_voice_session(
    session_id: str,
    service: VoiceServiceDep,
) -> dict:
    session = service.get_session(session_id)
    if session is None:
        return {"error": "not_found"}
    return {
        "session_id": session.session_id,
        "state": session.state.value,
        "interruptions": session.interruptions,
        "audio_chunks_received": session.audio_chunks_received,
        "audio_chunks_sent": session.audio_chunks_sent,
        "total_listen_duration": session.total_listen_duration,
        "total_speak_duration": session.total_speak_duration,
    }


@router.post("/sessions/{session_id}/end")
def end_voice_session(
    session_id: str,
    service: VoiceServiceDep,
) -> dict:
    try:
        session = service.end_session(session_id)
        return {"status": "ended", "state": session.state.value}
    except ValueError as e:
        return {"error": str(e)}


@router.websocket("/sessions/{session_id}/stream")
async def voice_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    service = get_voice_service()
    stt = get_stt_adapter()
    tts = get_tts_adapter()
    session = service.get_session(session_id)
    if session is None:
        await websocket.send_json({"error": "session_not_found"})
        await websocket.close()
        return

    service.transition_to(session_id, VoiceSessionState.listening)

    try:
        audio_buffer: list[bytes] = []
        while True:
            message = await websocket.receive()

            if message.get("type") == "websocket.receive":
                if "text" in message:
                    data = json.loads(message["text"])
                    if data.get("action") == "stop_listening":
                        if audio_buffer:
                            text = await stt.transcribe_stream(audio_buffer)
                            audio_buffer.clear()
                            service.transition_to(
                                session_id, VoiceSessionState.processing
                            )
                            await websocket.send_json({
                                "type": "transcription",
                                "text": text,
                            })
                            response_text = (
                                f"Merci pour votre message. Vous avez dit : {text[:50]}..."
                            )
                            audio = await tts.synthesize(response_text)
                            service.transition_to(
                                session_id, VoiceSessionState.speaking
                            )
                            await websocket.send_bytes(audio)
                            service.transition_to(
                                session_id, VoiceSessionState.listening
                            )
                        else:
                            await websocket.send_json({
                                "type": "info",
                                "message": "No audio received",
                            })

                    elif data.get("action") == "end_call":
                        service.end_session(session_id)
                        await websocket.send_json({"type": "session_ended"})
                        break

                elif "bytes" in message:
                    audio_buffer.append(message["bytes"])
                    service.transition_to(session_id, VoiceSessionState.listening)

    except WebSocketDisconnect:
        log.info("Voice session %s disconnected", session_id)
        service.end_session(session_id)
    except Exception as exc:
        log.error("Voice session %s error: %s", session_id, exc)
        service.end_session(session_id)
