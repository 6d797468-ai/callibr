from __future__ import annotations

from typing import Protocol


class STTAdapter(Protocol):
    """Speech-to-Text adapter. Transcribes audio bytes to text."""

    async def transcribe(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        """Transcribe audio data to text."""
        ...

    async def transcribe_stream(
        self, audio_chunks: list[bytes], sample_rate: int = 16000
    ) -> str:
        """Transcribe a stream of audio chunks (supports barge-in)."""
        ...


class TTSAdapter(Protocol):
    """Text-to-Speech adapter. Synthesizes text to audio bytes."""

    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        """Synthesize text to audio data."""
        ...

    async def synthesize_stream(
        self, text: str, voice: str = "default"
    ) -> list[bytes]:
        """Synthesize text to streaming audio chunks."""
        ...


class MockSTTAdapter:
    """Mock STT that returns predefined responses for testing."""

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self._responses = responses or {
            "default": "Bonjour, je cherche des informations sur mon compte.",
            "help": "Pouvez-vous m'aider avec mon problème ?",
            "yes": "Oui, d'accord.",
            "no": "Non, je ne suis pas d'accord.",
            "thanks": "Merci, c'est tout pour aujourd'hui.",
        }

    async def transcribe(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        if len(audio_data) < 100:
            return ""
        key = "default"
        if b"help" in audio_data[:100]:
            key = "help"
        elif b"yes" in audio_data[:100]:
            key = "yes"
        elif b"no" in audio_data[:100]:
            key = "no"
        elif b"thanks" in audio_data[:100]:
            key = "thanks"
        return self._responses.get(key, self._responses["default"])

    async def transcribe_stream(
        self, audio_chunks: list[bytes], sample_rate: int = 16000
    ) -> str:
        combined = b"".join(audio_chunks)
        return await self.transcribe(combined, sample_rate)

    def set_response(self, key: str, text: str) -> None:
        self._responses[key] = text


class MockTTSAdapter:
    """Mock TTS that returns empty audio for testing."""

    def __init__(self, chunk_size: int = 4096) -> None:
        self._chunk_size = chunk_size

    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        # Return a minimal WAV header + silence for testing
        duration_samples = int(len(text) * 0.1 * 16000)  # ~100ms per char
        wav = self._build_wav(duration_samples)
        return wav

    async def synthesize_stream(
        self, text: str, voice: str = "default"
    ) -> list[bytes]:
        wav = await self.synthesize(text, voice)
        return [wav[i : i + self._chunk_size] for i in range(0, len(wav), self._chunk_size)]

    def _build_wav(self, num_samples: int) -> bytes:
        import io
        import struct
        import wave

        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(16000)
            w.writeframes(struct.pack(f"<{num_samples}h", *([0] * num_samples)))
        return buf.getvalue()
