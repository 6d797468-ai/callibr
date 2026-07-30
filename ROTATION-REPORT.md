# Rotation Report — RC-2 / WP-002

**Date** : 2026-07-30

## Résultat automatique

| Variable | Ancienne clé | Nouvelle clé | Status |
|---|---|---|---|
| `CALLIBR_AUTH_SECRET` | `CLAUSEC_WcskJE...` | `DF++0BIgKmYEY5gk5czuEsg/...` | ✅ Remplacée |
| `CALLIBR_OPENAI_API_KEY` | `sk-proj-1RN29br6...` | _(vide — attend action)_ | 🔄 |
| `OPENROUTER_API_KEY` | `sk-or-v1-0b7f9db0...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_1` | `AIzaSyCpWrz8nxJ...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_2` | `AIzaSyC5ZPs0l8t...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_3` | `AIzaSyDSYS0cq-z...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_4` | `AIzaSyAXIEKPzIV...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_5` | `AIzaSyAHVFO-EkL...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_6` | `AIzaSyCSQK9F02w...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_7` | `AIzaSyCBiya7nMr...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_STUDIO_AI_API_KEY_8` | `AIzaSyAk0raJWFU...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_OAUTH_CLIENT_ID` | `410812683043-a2...` | _(vide — attend action)_ | 🔄 |
| `GOOGLE_OAUTH_CLIENT_SECRET_CODE` | `GOCSPX-R_1pmhSz...` | _(vide — attend action)_ | 🔄 |

## Scanner de secrets

- Fichiers scannés : 151
- Secrets détectés : **0**
- Résultat : **PASS** ✅

## Actions manuelles restantes

| Provider | Dashboard | Action |
|---|---|---|
| OpenAI | https://platform.openai.com/api-keys | Révoquer `sk-proj-1RN29br6...`, créer nouvelle clé |
| OpenRouter | https://openrouter.ai/keys | Révoquer `sk-or-v1-0b7f9db0...`, créer nouvelle clé |
| Google Cloud (Gemini ×8) | https://console.cloud.google.com/apis/credentials | Révoquer les 8 clés AIzaSy..., en créer de nouvelles |
| Google Cloud (OAuth) | https://console.cloud.google.com/apis/credentials | Révoquer le client OAuth, en créer un nouveau |
| Deepgram | https://console.deepgram.com | Créer une clé si CALLIBR_MOCK_STT=false |
| ElevenLabs | https://elevenlabs.io/app/settings/api-keys | Créer une clé si CALLIBR_MOCK_TTS=false |

## Prochaine étape

1. Révoquer chaque ancienne clé
2. Créer les nouvelles
3. Copier les nouvelles valeurs dans `.env`
4. Relancer `python -m engineering gate` -> **PASS**
