from __future__ import annotations

import logging
import os

import httpx

log = logging.getLogger(__name__)

DEEPGRAM_BASE = "https://api.deepgram.com/v1/listen"
ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"
ELEVENLABS_DEFAULT_VOICE = "pNInz6obpgDQGcFmaJgB"  # Adam


class DeepgramSTTAdapter:
    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.getenv("DEEPGRAM_API_KEY", "")

    async def transcribe(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        if not self._api_key:
            log.warning("Deepgram API key not set")
            return ""
        url = f"{DEEPGRAM_BASE}?model=whisper-large&language=fr&punctuate=true"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url,
                headers={
                    "Authorization": f"Token {self._api_key}",
                    "Content-Type": "audio/wav",
                },
                content=audio_data,
            )
            if resp.status_code != 200:
                log.error("Deepgram error: %s %s", resp.status_code, resp.text)
                return ""
            data = resp.json()
            channel = data.get("results", {}).get("channels", [{}])[0]
            alternatives = channel.get("alternatives", [{}])
            return alternatives[0].get("transcript", "") if alternatives else ""

    async def transcribe_stream(
        self, audio_chunks: list[bytes], sample_rate: int = 16000
    ) -> str:
        combined = b"".join(audio_chunks)
        return await self.transcribe(combined, sample_rate)


class ElevenLabsTTSAdapter:
    def __init__(
        self,
        api_key: str | None = None,
        voice_id: str | None = None,
    ) -> None:
        self._api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self._voice_id = voice_id or os.getenv(
            "ELEVENLABS_VOICE_ID", ELEVENLABS_DEFAULT_VOICE
        )

    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        if not self._api_key:
            log.warning("ElevenLabs API key not set")
            return b""
        effective_voice = self._voice_id if voice == "default" else voice
        url = f"{ELEVENLABS_BASE}/text-to-speech/{effective_voice}"
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                url,
                headers={
                    "xi-api-key": self._api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                    },
                },
            )
            if resp.status_code != 200:
                log.error("ElevenLabs error: %s %s", resp.status_code, resp.text)
                return b""
            return resp.content

    async def synthesize_stream(
        self, text: str, voice: str = "default"
    ) -> list[bytes]:
        audio = await self.synthesize(text, voice)
        if not audio:
            return []
        chunk_size = 4096
        return [audio[i : i + chunk_size] for i in range(0, len(audio), chunk_size)]
