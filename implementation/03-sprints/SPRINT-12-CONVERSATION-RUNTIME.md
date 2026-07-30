# Sprint 12 — Conversation Runtime

## Objectif

Rendre le `ConversationService` opérationnel de bout en bout : seed data chargé au démarrage, `ProcedureExecutor` auto-avançant par ordre, contrats Persona étendus aux traits client, et audit `ProcedureService` corrigé.

## Statut

**Terminé.**

## Livrables

### L1 — Module `callibr_seed` (package `packages/seed/`)

Nouveau package `callibr_seed` chargé via le `lifespan` FastAPI au démarrage de l'API.

**Catalogue de référence G1-SUPPORT-SAV :**

| Type | ID | Description |
|------|-----|-------------|
| Persona | `persona-sav-client-frustre-001` | Client frustré coopératif, traits frustration/coopération |
| Persona | `persona-sav-client-exigeant-001` | Client exigeant, traits exigence/impatience |
| Procédure | `proc-sav-retard-colis-001` | 5 étapes ordonnées pour retard colis |
| Procédure | `proc-sav-erreur-facturation-001` | 5 étapes ordonnées pour erreur facturation |
| Règle | `rule-identity-required` | Bloque les actions sensibles si identité non vérifiée |
| Règle | `rule-escalation-after-two-fails` | Déclenche escalade après 2 échecs de solution |
| Scénario | `sc-sav-retard-colis-v1` | Scénario conversation retard colis |
| Scénario | `sc-sav-erreur-facturation-v1` | Scénario conversation erreur facturation |

Le loader est idempotent : un second appel au démarrage ne duplique pas les données.

**Log de démarrage :**
```
callibr_seed: demo catalogue loaded — 2 personas, 2 procedures, 2 rules, 2 scenarios
Application startup complete.
```

### L2 — `ProcedureExecutor` : auto-advance par `order`

Avant S12, avancer une étape sans `next_step` déclaré terminait immédiatement l'exécution (`status=completed`). L'exécuteur cherche désormais la prochaine étape par `order` croissant lorsque `next_step` est absent.

**Comportement :**
- `next_step` explicite : prioritaire (rétrocompatible)
- `order` sans `next_step` : avancement automatique séquentiel
- Sans `order` ni `next_step` : fin d'exécution (comportement original)

**Smoke test :**
```
POST /procedures/proc-sav-retard-colis-001/executions
→ current_step=s-accueil, status=running

POST /procedures/executions/{id}/advance (step_id=s-accueil)
→ current_step=s-identite, completed=['s-accueil'], status=running  ✅
```

### L3 — `TraitName` : traits client

Ajout de 6 traits clients dans l'enum `TraitName` du contrat `PersonaTrait` :
`frustration`, `coopération`, `exigence`, `anxiété`, `satisfaction`, `impatience`.

Les 10 traits agent existants sont inchangés.

### L4 — `ProcedureService._append_audit` : correction AuditRecord

Le `type()` dynamique produisait un objet arbitraire stocké dans le `AuditEventStore`, non compatible avec `AuditRecord`. Remplacé par une instanciation directe de `AuditRecord`.

### L5 — Tests S12 : 18 nouveaux tests

Fichier : `tests/unit/test_s12_conversation_runtime.py`

| Classe | Tests |
|--------|-------|
| `TestSeedCatalogue` | 6 — chargement, idempotence, traits, steps, règles, références scénario |
| `TestProcedureExecutorAutoAdvance` | 4 — auto-advance, complétion, next_step prioritaire, sans order |
| `TestPersonaTraitClientEnum` | 7 — 6 traits client valides, 1 trait inconnu rejeté |
| `TestProcedureServiceAuditRecord` | 1 — AuditRecord Pydantic réel |

### L6 — Bugfixes gate pré-S12

Inclus dans S12 (identifiés lors du Runtime Integration Gate) :

| Bug | Fix |
|-----|-----|
| `app.include_router(module)` au lieu de `.router` | `main.py` L227-231 corrigé |
| `InMemoryScenarioRepository` — 404 pour tenants sans catalogue | Fallback catalogue partagé `_resolve()` |
| `get_persona_service` non importé dans `main.py` | Imports ajoutés |

## Résultats de test

```
Avant S12 : 134 collectés / 2 erreurs de collection
Après S12 : 167 passed, 3 skipped, 0 failed
```

Progression : **+33 tests** (18 S12 + 15 API débloqués)

## Validation de la chaîne complète

```
API démarre → seed catalogue chargé (log confirmé)             ✅
GET /api/v1/personas          → 2 personas                    ✅
GET /api/v1/procedures        → 2 procédures (5 steps each)   ✅
GET /api/v1/rules             → 2 règles                      ✅
GET /api/v1/scenarios/engine  → 2 scénarios                   ✅
POST /api/v1/conversations    → HTTP 201, persona + proc + rules assemblés ✅
POST /conversations/{id}/messages → HTTP 200, réponse MockAdapter ✅
GET  /conversations/{id}      → HTTP 200, 2 turns             ✅
```

## Risques résiduels post-S12

| # | Risque | Statut S12 |
|---|--------|-----------|
| R1 | Stores vides au démarrage | ✅ Résolu par `callibr_seed` |
| R2 | `current_step=None` après advance | ✅ Résolu par auto-advance par order |
| R3 | MockAdapter uniquement | 🟡 Documenté — LLM réel = S13+ |
| R4 | TraitName trop restrictive | ✅ Résolu — 6 traits client ajoutés |
