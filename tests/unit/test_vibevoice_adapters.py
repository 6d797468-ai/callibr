from __future__ import annotations

import io
import wave

import pytest
import websockets
from callibr_api.config import ConfigValidator, Settings
from callibr_voice import VibeVoiceASRAdapter, VibeVoiceTTSAdapter

ASR_OUTPUT = "Bonjour, comment puis-je vous aider ? Puis-je faire autre chose ?"

FAKE_ASR_INFER = """#!/usr/bin/env python3
import sys
import wave

audio = None
for i, arg in enumerate(sys.argv[1:]):
    if arg == "--audio":
        audio = sys.argv[2 + i]
if audio is None:
    print("missing --audio", file=sys.stderr)
    sys.exit(2)
w = wave.open(audio, "rb")
assert w.getsampwidth() == 2, "expected 16-bit WAV"
assert w.getnframes() > 0, "expected non-empty WAV"
print("%s" % "Bonjour, comment puis-je vous aider ?")
print("%s" % "Puis-je faire autre chose ?")
"""

FAKE_ASR_INFER_FAIL = """#!/usr/bin/env python3
import sys
print("boom", file=sys.stderr)
sys.exit(1)
"""


def _write_fake_bin(tmp_path: pytest.TempPathFactory, script: str, name: str) -> str:
    import stat

    path = tmp_path / name
    path.write_text(script)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return str(path)


class TestVibeVoiceASRAdapter:
    @pytest.mark.asyncio
    async def test_transcribe_returns_cli_stdout(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        bin_path = _write_fake_bin(tmp_path, FAKE_ASR_INFER, "asr_infer")
        adapter = VibeVoiceASRAdapter(
            bin_path=bin_path,
            vae_model="/models/vae.gguf",
            lm_model="/models/lm.gguf",
        )
        result = await adapter.transcribe(b"\x00" * 32000, sample_rate=16000)
        assert result == ASR_OUTPUT

    @pytest.mark.asyncio
    async def test_transcribe_stream_concatenates_chunks(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        bin_path = _write_fake_bin(tmp_path, FAKE_ASR_INFER, "asr_infer")
        adapter = VibeVoiceASRAdapter(
            bin_path=bin_path,
            vae_model="/models/vae.gguf",
            lm_model="/models/lm.gguf",
        )
        chunks = [b"\x00" * 16000, b"\x00" * 16000]
        result = await adapter.transcribe_stream(chunks)
        assert result == ASR_OUTPUT

    @pytest.mark.asyncio
    async def test_transcribe_empty_audio_returns_empty(self) -> None:
        adapter = VibeVoiceASRAdapter(
            bin_path="/bin/asr_infer",
            vae_model="/models/vae.gguf",
            lm_model="/models/lm.gguf",
        )
        assert await adapter.transcribe(b"") == ""

    @pytest.mark.asyncio
    async def test_unconfigured_returns_empty(self) -> None:
        adapter = VibeVoiceASRAdapter(bin_path="", vae_model="", lm_model="")
        assert not adapter.is_configured()
        assert await adapter.transcribe(b"\x00" * 32000) == ""

    @pytest.mark.asyncio
    async def test_nonzero_exit_returns_empty(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        bin_path = _write_fake_bin(tmp_path, FAKE_ASR_INFER_FAIL, "asr_infer_fail")
        adapter = VibeVoiceASRAdapter(
            bin_path=bin_path,
            vae_model="/models/vae.gguf",
            lm_model="/models/lm.gguf",
        )
        assert await adapter.transcribe(b"\x00" * 32000) == ""


class TestVibeVoiceTTSAdapter:
    @pytest.mark.asyncio
    async def test_synthesize_returns_wav_with_pcm(self) -> None:
        pcm = (b"\x00\x00" * 4000) + b"\xff\x7f" * 100
        text_received = []

        async def handler(ws):
            text_received.append(ws.request.path)
            await ws.send('{"type":"log","event":"backend_request_received"}')
            await ws.send(pcm)
            await ws.close()

        server = await websockets.serve(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            adapter = VibeVoiceTTSAdapter(ws_url=f"ws://127.0.0.1:{port}/stream")
            wav = await adapter.synthesize("Bonjour")
            assert "text=Bonjour" in text_received[0]
            with wave.open(io.BytesIO(wav), "rb") as w:
                assert w.getframerate() == 24000
                assert w.getsampwidth() == 2
                assert w.getnchannels() == 1
                assert w.readframes(w.getnframes()) == pcm
        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_synthesize_voice_param_appended(self) -> None:
        paths = []

        async def handler(ws):
            paths.append(ws.request.path)
            await ws.send(b"\x00\x00" * 100)
            await ws.close()

        server = await websockets.serve(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            adapter = VibeVoiceTTSAdapter(ws_url=f"ws://127.0.0.1:{port}/stream")
            await adapter.synthesize("Bonjour", voice="en-Carter_man")
            assert "voice=en-Carter_man" in paths[0]
            await adapter.synthesize("Bonjour", voice="default")
            assert "voice=" not in paths[1]
        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_synthesize_stream_reassembles_pcm(self) -> None:
        pcm = b"\x00\x00" * 5000

        async def handler(ws):
            await ws.send(pcm)
            await ws.close()

        server = await websockets.serve(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            adapter = VibeVoiceTTSAdapter(ws_url=f"ws://127.0.0.1:{port}/stream")
            chunks = await adapter.synthesize_stream("Test")
            assert chunks
            assert b"".join(chunks) == pcm
        finally:
            server.close()
            await server.wait_closed()

    @pytest.mark.asyncio
    async def test_synthesize_no_audio_returns_empty(self) -> None:
        async def handler(ws):
            await ws.close()

        server = await websockets.serve(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            adapter = VibeVoiceTTSAdapter(ws_url=f"ws://127.0.0.1:{port}/stream")
            assert await adapter.synthesize("Bonjour") == b""
            assert await adapter.synthesize_stream("Bonjour") == []
        finally:
            server.close()
            await server.wait_closed()


class TestConfigValidator:
    def test_vibevoice_stt_requires_engine_paths(self) -> None:
        settings = Settings(
            voice_stt_provider="vibevoice",
            vibevoice_asr_bin="",
            vibevoice_asr_vae_model="",
            vibevoice_asr_lm_model="",
        )
        errors = ConfigValidator().validate(settings)
        assert any("vibevoice" in str(err) for err in errors)

    def test_vibevoice_stt_valid_when_paths_set(self) -> None:
        settings = Settings(
            voice_stt_provider="vibevoice",
            vibevoice_asr_bin="/bin/asr_infer",
            vibevoice_asr_vae_model="/models/vae.gguf",
            vibevoice_asr_lm_model="/models/lm.gguf",
        )
        errors = ConfigValidator().validate(settings)
        assert not any("vibevoice" in str(err) for err in errors)
