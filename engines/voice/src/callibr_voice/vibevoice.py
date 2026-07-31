from __future__ import annotations

import asyncio
import io
import logging
import os
import tempfile
import wave
from pathlib import Path

log = logging.getLogger(__name__)

VIBEVOICE_TTS_SAMPLE_RATE = 24000


def pcm16_to_wav(pcm_data: bytes, sample_rate: int) -> bytes:
    """Wrap raw 16-bit mono PCM into a WAV file."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm_data)
    return buf.getvalue()


class VibeVoiceASRAdapter:
    """STT backed by the VibeASR.cpp CPU inference engine (asr_infer CLI).

    The engine runs fully locally: ~1.58 GB BitNet-quantized models, real-time
    on 3-4 CPU threads, no GPU required.
    """

    def __init__(
        self,
        bin_path: str | os.PathLike[str],
        vae_model: str | os.PathLike[str],
        lm_model: str | os.PathLike[str],
        threads: int = 4,
        timeout_seconds: float = 300.0,
    ) -> None:
        self._bin = os.fspath(bin_path)
        self._vae_model = os.fspath(vae_model)
        self._lm_model = os.fspath(lm_model)
        self._threads = threads
        self._timeout_seconds = timeout_seconds

    def is_configured(self) -> bool:
        return bool(self._bin and self._vae_model and self._lm_model)

    async def transcribe(self, audio_data: bytes, sample_rate: int = 16000) -> str:
        if not audio_data or not self.is_configured():
            log.warning("VibeVoice ASR: missing audio or engine paths")
            return ""
        wav = pcm16_to_wav(audio_data, sample_rate)
        return await self._run_asr_infer(wav)

    async def transcribe_stream(
        self, audio_chunks: list[bytes], sample_rate: int = 16000
    ) -> str:
        return await self.transcribe(b"".join(audio_chunks), sample_rate)

    async def _run_asr_infer(self, wav_data: bytes) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            wav_path = Path(tmp) / "input.wav"
            wav_path.write_bytes(wav_data)
            proc = await asyncio.create_subprocess_exec(
                self._bin,
                "--vae-model",
                self._vae_model,
                "--lm-model",
                self._lm_model,
                "--audio",
                str(wav_path),
                "-t",
                str(self._threads),
                "--greedy",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=self._timeout_seconds
                )
            except TimeoutError:
                proc.kill()
                log.error("VibeVoice ASR: inference timed out after %ss", self._timeout_seconds)
                return ""
        if proc.returncode != 0:
            detail = stderr.decode(errors="replace").strip()[-500:]
            log.error("VibeVoice ASR: asr_infer exited %s: %s", proc.returncode, detail)
            return ""
        text = stdout.decode(errors="replace").strip()
        return " ".join(text.split())


class VibeVoiceTTSAdapter:
    """TTS backed by the VibeVoice-Realtime streaming WebSocket server.

    The server is started separately (see docs); this adapter streams the
    request through its WebSocket endpoint and reassembles 24 kHz PCM16 audio.
    """

    def __init__(
        self,
        ws_url: str = "ws://localhost:3000/stream",
        voice: str | None = None,
    ) -> None:
        self._ws_url = ws_url.rstrip("/")
        self._voice = voice

    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        pcm = await self._receive_pcm(text, voice)
        if not pcm:
            return b""
        return pcm16_to_wav(pcm, VIBEVOICE_TTS_SAMPLE_RATE)

    async def synthesize_stream(
        self, text: str, voice: str = "default"
    ) -> list[bytes]:
        pcm = await self._receive_pcm(text, voice)
        if not pcm:
            return []
        chunk_size = 4096
        return [pcm[i : i + chunk_size] for i in range(0, len(pcm), chunk_size)]

    async def _receive_pcm(self, text: str, voice: str) -> bytes:
        import urllib.parse

        import websockets

        query = f"?text={urllib.parse.quote(text)}"
        effective_voice = voice if voice != "default" else self._voice
        if effective_voice:
            query += f"&voice={urllib.parse.quote(effective_voice)}"
        url = f"{self._ws_url}{query}"

        chunks: list[bytes] = []
        try:
            async with websockets.connect(url, open_timeout=30, ping_interval=None) as ws:
                async for message in ws:
                    if isinstance(message, (bytes, bytearray)):
                        chunks.append(bytes(message))
        except Exception as exc:  # noqa: BLE001
            log.error("VibeVoice TTS: WebSocket error: %s", exc)
            return b""
        return b"".join(chunks)
