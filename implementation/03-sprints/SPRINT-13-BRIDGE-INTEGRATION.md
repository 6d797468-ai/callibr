# Sprint 13 — Intégration SimulationService ↔ ConversationService

## Objectif

Brancher le moteur de simulation sur le `ConversationService` via un **Bridge pattern non-breaking** : réponses client générées par le pipeline LLM/Persona/Procedure/Rule, rapport de session enrichi avec la progression procédurale, et migrations Alembic pour les nouvelles colonnes PostgreSQL.

## Statut

**Terminé.**

## Livrables

### L1 — Bridge `SimulationService` ↔ `ConversationService`

**Fichiers :** `engines/simulation/src/callibr_simulation/service.py`, `packages/contracts/src/callibr_contracts/simulation.py`

Architecture **Bridge optionnel** : le `ConversationService` est injecté comme dépendance optionnelle (`None` = comportement original inchangé). Un `SCENARIO_BRIDGE_MAP` mappe les IDs simulation vers les IDs du moteur de scénarios.

```python
SCENARIO_BRIDGE_MAP = {
    "sav-retard-colis-001": "sc-sav-retard-colis-v1",
    "sav-erreur-facturation-001": "sc-sav-erreur-facturation-v1",
}
```

**Comportement bridge activé :**
- `start_session()` → appelle `ConversationService.start_conversation()` et stocke `conversation_session_id` + `procedure_execution_id` dans `SimulationSession`
- `send_message()` → génère la réponse client via `ConversationService.process_message()` (LLM mock → futur LLM réel)
- `get_session_report()` → inclut `procedure_progress` (étapes + statuts) + `procedure_execution_id`

**Fallback garanti :** toute exception du `ConversationService` est interceptée → retour aux réponses statiques. Aucune régression possible.

### L2 — Nouveaux champs `SimulationSession` et `SessionReport`

| Modèle | Champ | Type | Description |
|--------|-------|------|-------------|
| `SimulationSession` | `conversation_session_id` | `str \| None` | ID session ConversationService |
| `SimulationSession` | `procedure_execution_id` | `str \| None` | ID exécution procédure |
| `SessionReport` | `procedure_execution_id` | `str \| None` | ID exécution procédure |
| `SessionReport` | `procedure_progress` | `list[dict]` | Étapes complétées/en cours |

### L3 — Wiring `dependencies.py`

`get_simulation_service()` reçoit maintenant `conversation_service=get_conversation_service()`.

### L4 — Migration Alembic 002

**Fichier :** `infrastructure/postgres/alembic/versions/002_bridge_columns.py`

```sql
-- upgrade
ALTER TABLE simulation_sessions
    ADD COLUMN IF NOT EXISTS conversation_session_id TEXT,
    ADD COLUMN IF NOT EXISTS procedure_execution_id TEXT;

CREATE INDEX IF NOT EXISTS simulation_sessions_conv_session_idx
    ON simulation_sessions (conversation_session_id)
    WHERE conversation_session_id IS NOT NULL;

-- downgrade
DROP INDEX IF EXISTS simulation_sessions_conv_session_idx;
ALTER TABLE simulation_sessions
    DROP COLUMN IF EXISTS conversation_session_id,
    DROP COLUMN IF EXISTS procedure_execution_id;
```

### L5 — Tests S13 : 12 nouveaux tests

**Fichier :** `tests/unit/test_s13_simulation_bridge.py`

| Classe | Tests |
|--------|-------|
| `TestScenarioBridgeMap` | 3 — mapping correct des deux scénarios |
| `TestBridgeDisabled` | 3 — comportement original préservé |
| `TestBridgeEnabled` | 6 — activation, LLM reply, procedure_progress, fallbacks |

## Validation

### Résultats de test

```
Avant S13 : 167 passed
Après S13 : 179 passed, 3 skipped, 0 failed
+12 tests, 0 régression
```

### Smoke test API bridge

```
POST /api/v1/simulations
→ conversation_session_id=conv_7e7efbf3ab45457...  ✅
→ procedure_execution_id=proc-exec_11ac218728...   ✅

POST /api/v1/simulations/{id}/messages
→ customer_message="Ceci est une réponse simulée."
→ bridge_active=True                                ✅

GET /api/v1/simulations/{id}/report
→ procedure_execution_id=proc-exec_11ac218728...   ✅
→ procedure_progress=[{step_id: "s-accueil", status: "active"}]  ✅
```

## Architecture après S13

```
POST /simulations
    └── SimulationService.start_session()
            ├── ScenarioRepository.get()          ← catalogue simulation (InMemory)
            └── [bridge] ConversationService.start_conversation()
                    ├── ScenarioService.compose() ← catalogue engine (seed)
                    ├── ProcedureService.start()  ← proc-sav-retard-colis-001
                    └── PersonaService.build_prompt_context()

POST /simulations/{id}/messages
    └── SimulationService.send_message()
            ├── EvaluationService.evaluate_turn() ← scoring critères métier
            └── [bridge] ConversationService.process_message()
                    └── MockAdapter.generate()    ← LLM (réel = S14+)

GET /simulations/{id}/report
    └── SessionReport
            ├── criteria, score, strengths/risks  ← EvaluationService
            ├── procedure_execution_id             ← bridge
            └── procedure_progress [{step_id, status, score}]  ← ProcedureService
```

## Risques résiduels

| # | Risque | Statut |
|---|--------|--------|
| R1 | MockAdapter uniquement | 🟡 S14+ — LLM réel (OpenAI/Anthropic adapter) |
| R2 | PostgreSQL non testé automatiquement | 🟡 tests integration skip sans DB |
| R3 | Seed InMemory perdu au redémarrage | 🟡 Mitigé par lifespan seed — résolution en S15 (persistence seed PostgreSQL) |
