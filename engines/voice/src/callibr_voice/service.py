from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from callibr_voice.models import (
    AudioChunk,
    VoiceConfig,
    VoiceSession,
    VoiceSessionState,
)


class VoiceSessionService:
    """Manages voice session lifecycle and state transitions."""

    def __init__(self) -> None:
        self._sessions: dict[str, VoiceSession] = {}

    def create_session(
        self,
        simulation_session_id: str,
        config: VoiceConfig | None = None,
    ) -> VoiceSession:
        session_id = f"voice_{uuid.uuid4().hex[:16]}"
        session = VoiceSession(
            session_id=session_id,
            simulation_session_id=simulation_session_id,
            state=VoiceSessionState.idle,
            config=config or VoiceConfig(),
            started_at=datetime.now(UTC).isoformat(),
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> VoiceSession | None:
        return self._sessions.get(session_id)

    def transition_to(
        self, session_id: str, state: VoiceSessionState
    ) -> VoiceSession:
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(f"Voice session not found: {session_id}")

        update: dict[str, Any] = {"state": state}

        if state == VoiceSessionState.listening or state == VoiceSessionState.speaking:
            pass
        elif state == VoiceSessionState.ended:
            update["ended_at"] = datetime.now(UTC).isoformat()
        elif state == VoiceSessionState.interrupted:
            session.interruptions += 1

        updated = session.model_copy(update=update)
        self._sessions[session_id] = updated
        return updated

    def record_chunk_received(self, session_id: str, chunk: AudioChunk) -> None:
        session = self._sessions.get(session_id)
        if session is None:
            return
        updated = session.model_copy(
            update={
                "audio_chunks_received": session.audio_chunks_received + 1,
                "total_listen_duration": session.total_listen_duration
                + chunk.duration_seconds,
            }
        )
        self._sessions[session_id] = updated

    def record_chunk_sent(self, session_id: str, chunk: AudioChunk) -> None:
        session = self._sessions.get(session_id)
        if session is None:
            return
        updated = session.model_copy(
            update={
                "audio_chunks_sent": session.audio_chunks_sent + 1,
                "total_speak_duration": session.total_speak_duration
                + chunk.duration_seconds,
            }
        )
        self._sessions[session_id] = updated

    def end_session(self, session_id: str) -> VoiceSession:
        return self.transition_to(session_id, VoiceSessionState.ended)

    def clear(self) -> None:
        self._sessions.clear()
