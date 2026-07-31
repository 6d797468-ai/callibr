# Implementation Status

Mise a jour : 2026-07-31

## Baseline

- Release : **v0.1.0-rc3**
- Commit : `d29b82f` (squash PR #5)
- CI : 5/5 pipelines verts
- GitHub : PR #1 a #5 fusionnees

## Etat Produit

- First Run Wizard ✅
- Guided Simulation ✅
- Voice Runtime v1 ✅
- Live Coaching ✅
- Executive Report PDF ✅
- Feedback ✅
- Replay ✅
- PostgreSQL Persistence ✅
- **Pilot Dashboard (EP-007 WP-001) ✅** — cockpit 4 widgets (KPI, funnel 6 etapes, activite recente, alertes), sans metriques techniques, alimente par les stores de persistance (memory / postgres via `PersistenceFactory`)
- **Error UX (EP-007 WP-002) ✅** — aucun ecran ne montre plus d'erreur technique brute : taxonomy frontend (8 cas : LLM, STT/TTS, timeout, reseau, scenario introuvable, rapport indisponible, PostgreSQL, inattendu), corps d'erreur backend structure (`code/title/explanation/action/retryable/trace_id`), handlers globaux (Exception, HTTPException, 422), ErrorPanel + ErrorBoundary + bouton de reprise partout, timeout 30s cote client
- **Empty States (EP-007 WP-003) ✅** — composant EmptyState uniforme sur 8 vues (Dashboard, Simulations, Rapports, Replay, Avis, Analytics, Scenarios, Voix), CTA unique, progressive disclosure, navigation "Mon activite" ; 3 nouveaux endpoints de liste (`/simulations`, `/reports`, `/voice/sessions`) ; bug ingere d'events corrige (modeles de route au niveau module)
- **VibeVoice local voice ✅** — STT et TTS 100 % locaux, sans cle API ni GPU : STT via VibeASR.cpp (`asr_infer`, modeles BitNet GGUF ~1.6 Go, CPU) ; TTS via le serveur WebSocket VibeVoice-Realtime-0.5B (streaming ~300 ms). Adapters `VibeVoiceASRAdapter` / `VibeVoiceTTSAdapter`, selection par `CALLIBR_VOICE_STT_PROVIDER` / `CALLIBR_VOICE_TTS_PROVIDER` (mock | deepgram | elevenlabs | vibevoice), fallback Mock si mal configure ; verification E2E locale reelle (asr_infer compile, models telecharges, transcription de parole reelle OK)

## Qualite

- 381 tests unitaires + API, 23 tests integration PostgreSQL validee
- CI verte (Backend Quality, Frontend Build, Security Scan, Shell Validation, PostgreSQL Integration)
- Architecture gelee
- Engineering Score : 83.2 % (release gate CI — hausse apres WP-001)

## Dette Planifiee

- EP-010 Architecture Cleanup : 12 violations d'architecture + 1 capability < 50 %, traitees apres le premier pilote (aucun blocage EP-007/EP-008 identifie)

## Risques Ouverts

- Aucun P0 technique
- Validation utilisateur reelle non commencee
- Pas encore de donnees pilote
