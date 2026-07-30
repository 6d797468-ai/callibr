from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class VoiceSessionState(StrEnum):
    idle = "idle"
    listening = "listening"
    processing = "processing"
    speaking = "speaking"
    interrupted = "interrupted"
    paused = "paused"
    ended = "ended"


class AudioChunk(BaseModel):
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    duration_seconds: float = 0.0
    is_final: bool = False


class VoiceConfig(BaseModel):
    input_sample_rate: int = 16000
    output_sample_rate: int = 24000
    silence_timeout_seconds: float = 2.0
    max_session_duration_seconds: int = 600
    barge_in_enabled: bool = True
    language: str = "fr-FR"
    vad_enabled: bool = True


class VoiceSession(BaseModel):
    session_id: str
    simulation_session_id: str
    state: VoiceSessionState = VoiceSessionState.idle
    config: VoiceConfig = Field(default_factory=VoiceConfig)
    started_at: str = ""
    ended_at: str = ""
    audio_chunks_received: int = 0
    audio_chunks_sent: int = 0
    total_listen_duration: float = 0.0
    total_speak_duration: float = 0.0
    interruptions: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)
