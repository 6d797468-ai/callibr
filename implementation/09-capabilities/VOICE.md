# VOICE — Voice Runtime (STT / TTS)

Mise a jour : 2026-07-31

## Definition

Capacite de conversation vocale : transcription de la parole (STT), synthese
vocale (TTS), gestion de session et barge-in. Le parcours voix fonctionne avec
des fournisseurs cloud (Deepgram / ElevenLabs) **ou** en 100 % local sans cle
API ni GPU via VibeVoice (Microsoft).

## Stabilite

Le contrat d'adaptateur (`STTAdapter` / `TTSAdapter`) est stable. Les
fournisseurs sont interchangeables par configuration, sans changement de code.

## Fournisseurs

| Provider | STT | TTS | Cle API | GPU |
| --- | --- | --- | --- | --- |
| `mock` (defaut) | `MockSTTAdapter` | `MockTTSAdapter` | non | non |
| `deepgram` | `DeepgramSTTAdapter` | — | `DEEPGRAM_API_KEY` | non |
| `elevenlabs` | — | `ElevenLabsTTSAdapter` | `ELEVENLABS_API_KEY` | non |
| `vibevoice` | `VibeVoiceASRAdapter` (VibeASR.cpp) | `VibeVoiceTTSAdapter` (Realtime-0.5B WS) | non | non |

## Configuration

Selection par environnement :

- `CALLIBR_VOICE_STT_PROVIDER=mock|deepgram|vibevoice` (defaut : `mock`)
- `CALLIBR_VOICE_TTS_PROVIDER=mock|elevenlabs|vibevoice` (defaut : `mock`)
- `CALLIBR_MOCK_STT` / `CALLIBR_MOCK_TTS` (bool, retrocompatibles) : force Mock
- `CALLIBR_VIBEVOICE_ASR_BIN` : chemin du binaire `asr_infer`
- `CALLIBR_VIBEVOICE_ASR_VAE_MODEL` : `vibeasr-vae-encoder-i8_s.gguf`
- `CALLIBR_VIBEVOICE_ASR_LM_MODEL` : `vibeasr-lm-i2_s-embed-q6_k.gguf`
- `CALLIBR_VIBEVOICE_ASR_THREADS` (defaut : `4`)
- `CALLIBR_VIBEVOICE_TTS_URL` : `ws://localhost:3000/stream`

Le provider `vibevoice` non configure (chemins manquants) retombe sur Mock avec
un warning ; le `ConfigValidator` signale la configuration incomplète.

## STT local — VibeASR.cpp (CPU)

Inference ASR entièrement locale, temps reel sur CPU (3-4 threads) :
modeles BitNet heterogenes I8_S (VAE) + I2_S (LM), ~1.58 Go, 50+ langues.

Setup (une fois) :

```bash
git clone --recursive https://github.com/microsoft/VibeASR.cpp.git
cd VibeASR.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)
pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/VibeVoice-ASR-BitNet', local_dir='models/vibeasr', ignore_patterns=['*.safetensors','*.bin','*.pt'])"
```

Verification :

```bash
./build/bin/asr_infer --vae-model models/vibeasr/vibeasr-vae-encoder-i8_s.gguf \
    --lm-model models/vibeasr/vibeasr-lm-i2_s-embed-q6_k.gguf \
    --audio input.wav -t 4 --greedy
```

## TTS local — VibeVoice-Realtime-0.5B (WebSocket)

Serveur de streaming TTS (~200-300 ms premier chunk, PCM16 24 kHz, mono).
Gros volume d'installation (torch + transformers, ~2 Go de modeles) :
a installer sur une machine avec ~8 Go de disque libre.

```bash
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice
pip install -e ".[streamingtts]"
python demo/vibevoice_realtime_demo.py --port 3000 \
    --model_path microsoft/VibeVoice-Realtime-0.5B --device cpu
```

`VibeVoiceTTSAdapter` se connecte a `ws://localhost:3000/stream?text=...`,
reassemble les trames PCM16 et renvoie un WAV 24 kHz (ou un flux de chunks).
Voix experimentales FR/DE/... disponibles via
`demo/download_experimental_voices.sh` ; passer le nom de voix par
`CALLIBR_VIBEVOICE_TTS_VOICE` ou l'argument `voice` de l'API.

## Tests

`tests/unit/test_vibevoice_adapters.py` — 11 tests : CLI `asr_infer` stube
(WAV valide + transcript), serveur WebSocket stube (trames texte+binaire),
validateur de configuration. Suite complete : 381 tests unitaires + API,
23 integration PostgreSQL.

## Notes de performance (machine demo 4 threads, 11 Go RAM)

- ASR : ~5 s d'audio en ~57 s (RTF ~11). Sufoisant pour des echanges courts ;
  sur EPYC 24 cœurs / i7-13700 le moteur est temps reel (RTF < 1).
- TTS : temps reel CPU attendu (~0.5B params).
