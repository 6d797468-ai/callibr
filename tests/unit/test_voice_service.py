from __future__ import annotations

import pytest
from callibr_voice import (
    AudioChunk,
    MockSTTAdapter,
    MockTTSAdapter,
    VoiceConfig,
    VoiceSessionService,
    VoiceSessionState,
)


class TestVoiceSessionService:
    def test_create_session(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        assert session.session_id.startswith("voice_")
        assert session.simulation_session_id == "sim_test_001"
        assert session.state == VoiceSessionState.idle
        assert session.started_at != ""

    def test_get_session_returns_none_for_missing(self) -> None:
        service = VoiceSessionService()
        assert service.get_session("nonexistent") is None

    def test_get_session_returns_created_session(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        assert service.get_session(session.session_id) is not None

    def test_transition_to_listening(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        updated = service.transition_to(session.session_id, VoiceSessionState.listening)
        assert updated.state == VoiceSessionState.listening

    def test_transition_to_ended_sets_ended_at(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        updated = service.transition_to(session.session_id, VoiceSessionState.ended)
        assert updated.state == VoiceSessionState.ended
        assert updated.ended_at != ""

    def test_transition_to_interrupted_increments_count(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        service.transition_to(session.session_id, VoiceSessionState.interrupted)
        updated = service.transition_to(session.session_id, VoiceSessionState.interrupted)
        assert updated.interruptions == 2

    def test_transition_raises_for_missing_session(self) -> None:
        service = VoiceSessionService()
        with pytest.raises(ValueError, match="Voice session not found"):
            service.transition_to("nonexistent", VoiceSessionState.listening)

    def test_record_chunk_received(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        chunk = AudioChunk(data=b"test", duration_seconds=0.5)
        service.record_chunk_received(session.session_id, chunk)
        updated = service.get_session(session.session_id)
        assert updated is not None
        assert updated.audio_chunks_received == 1
        assert updated.total_listen_duration == 0.5

    def test_record_chunk_sent(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        chunk = AudioChunk(data=b"test", duration_seconds=1.0)
        service.record_chunk_sent(session.session_id, chunk)
        updated = service.get_session(session.session_id)
        assert updated is not None
        assert updated.audio_chunks_sent == 1
        assert updated.total_speak_duration == 1.0

    def test_end_session(self) -> None:
        service = VoiceSessionService()
        session = service.create_session("sim_test_001")
        ended = service.end_session(session.session_id)
        assert ended.state == VoiceSessionState.ended

    def test_clear_resets_all_sessions(self) -> None:
        service = VoiceSessionService()
        service.create_session("sim_test_001")
        service.create_session("sim_test_002")
        service.clear()
        assert len(service._sessions) == 0

    def test_create_with_custom_config(self) -> None:
        service = VoiceSessionService()
        config = VoiceConfig(language="en-US", silence_timeout_seconds=3.0)
        session = service.create_session("sim_test_001", config=config)
        assert session.config.language == "en-US"
        assert session.config.silence_timeout_seconds == 3.0


class TestMockSTTAdapter:
    @pytest.mark.asyncio
    async def test_transcribe_default(self) -> None:
        adapter = MockSTTAdapter()
        result = await adapter.transcribe(b"\x00" * 200)
        assert result == "Bonjour, je cherche des informations sur mon compte."

    @pytest.mark.asyncio
    async def test_transcribe_empty_audio(self) -> None:
        adapter = MockSTTAdapter()
        result = await adapter.transcribe(b"\x00" * 50)
        assert result == ""

    @pytest.mark.asyncio
    async def test_set_response(self) -> None:
        adapter = MockSTTAdapter()
        adapter.set_response("yes", "Oui, tout à fait.")
        result = await adapter.transcribe(b"yes" + b"\x00" * 200)
        assert result == "Oui, tout à fait."

    @pytest.mark.asyncio
    async def test_transcribe_stream(self) -> None:
        adapter = MockSTTAdapter()
        chunks = [b"help" + b"\x00" * 100]
        result = await adapter.transcribe_stream(chunks)
        assert result == "Pouvez-vous m'aider avec mon problème ?"


class TestMockTTSAdapter:
    @pytest.mark.asyncio
    async def test_synthesize_returns_wav_data(self) -> None:
        adapter = MockTTSAdapter()
        result = await adapter.synthesize("Bonjour")
        assert len(result) > 44  # WAV header (44 bytes) + samples
        assert result[:4] == b"RIFF"
        assert result[8:12] == b"WAVE"

    @pytest.mark.asyncio
    async def test_synthesize_stream_returns_chunks(self) -> None:
        adapter = MockTTSAdapter(chunk_size=32)
        chunks = await adapter.synthesize_stream("Test message")
        assert len(chunks) >= 1

    @pytest.mark.asyncio
    async def test_synthesize_stream_returns_all_data(self) -> None:
        adapter = MockTTSAdapter(chunk_size=100)
        chunks = await adapter.synthesize_stream("Hello world")
        combined = b"".join(chunks)
        assert combined[:4] == b"RIFF"
