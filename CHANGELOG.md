# Changelog

## v0.1.0-rc1 (2026-07-30)

### Architecture
- Conversation/Simulation Director — state machine à 6 étages avec adaptation de difficulté
- Response Planner — planification déterministe (intention, ton, contraintes)
- Response Validator — 9 vérifications déterministes, boucle de regénération
- Voice Runtime — STT/TTS (Mock + Deepgram + ElevenLabs), WebSocket streaming
- Frontend Voice UI — push-to-talk, MediaRecorder, état du micro
- AI Runtime — Token Budget, Context Reduction, Safety Validation, LLM Router
- Architecture gelée — plus de nouveaux moteurs, protocoles ou couches avant le pilote

### Integration
- Director + Planner injectés dans SimulationService.send_message()
- Validateur branché avec boucle de retry (max 2 tentatives)
- plan_context ajouté à ConversationContext
- current_step piloté par DirectorDecision.next_stage

### Security
- ConfigValidator au démarrage — échoue explicitement si variable manquante
- Secret Scanner — 20 patterns (API keys, tokens, clés privées)
- Secret Scanner intégré au Release Gate
- Configuration unifiée via Pydantic Settings
- Toutes les variables documentées dans .env.example (valeurs vides)
- docker-compose.yml corrigé (.env au lieu de .env.example)

### Telemetry
- validation_results_total (Prometheus counter)
- Dashboard, feedback, readiness, export PDF

### Tests
- 318 tests unitaires, 3 skipped
- Tests d'intégration ✅
- Tests d'architecture ✅
- Lint: 0 erreur sur les fichiers modifiés
