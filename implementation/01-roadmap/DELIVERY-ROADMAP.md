# Delivery Roadmap

Mise a jour : 2026-07-31

Cadence recommandee : sprint de 2 semaines.

## Baseline actuelle — v0.1.0-rc3

La version **v0.1.0-rc3** (2026-07-31) est la reference immuable. Elle couvre les
milestones M0 a M4 ci-dessous ainsi que la persistance PostgreSQL durable (EP-006).

Etat : architecture gelee, 351 tests unitaires + integration PostgreSQL valides,
5 pipelines CI verts (Backend Quality, Frontend Build, Security Scan, Shell
Validation, PostgreSQL Integration), protection de `main` adaptee au developpement
solo (checks obligatoires, merge via PR, push direct interdit).

A partir de maintenant :

- toutes les nouvelles fonctionnalites partent de RC3 ;
- les moteurs principaux restent gelee ;
- toute evolution doit etre justifiee par un besoin utilisateur, un retour pilote
  ou un bug.

## Vue Globale

| Sprint | Phase | Objectif | Livrable demo |
| --- | --- | --- | --- |
| 00 | P0 | Bootstrap monorepo | App demarre localement |
| 01 | P1 | Kernel minimal | Commands, events, config, logging |
| 02 | P1 | Identity & tenant context | utilisateur demo authentifie |
| 03 | P2 | Session & conversation | chat de simulation |
| 04 | P2 | Scenario & persona | client simule contextualise |
| 05 | P3 | CRM fictif | dossier client consultable |
| 06 | P3 | Actions metier | verify identity, create ticket |
| 07 | P3 | Procedure engine | checklist et obligations |
| 08 | P4 | Evaluation QA | score final rule-based |
| 09 | P4 | Coaching feedback | feedback et recommandations |
| 10 | P5 | Dashboard minimal | historique et KPI simples |
| 11 | P6 | Observabilite & hardening | logs, metrics, traces de base |
| 12 | P6 | Release candidate MVP | demo stable et documentee |

## Milestone M0 — Repository Ready

Inclut :

- structure monorepo ;
- backend FastAPI ;
- frontend minimal ;
- PostgreSQL ;
- Redis ;
- tests ;
- lint ;
- docker compose.

## Milestone M1 — Simulation Loop

Inclut :

- session ;
- message ;
- persona ;
- scenario ;
- conversation timeline.

## Milestone M2 — Business Actions

Inclut :

- CRM fictif ;
- action engine ;
- procedure engine ;
- event trail.

## Milestone M3 — Learning Value

Inclut :

- evaluation QA ;
- feedback ;
- rapport ;
- progression.

## Milestone M4 — MVP Release Candidate

Inclut :

- observabilite minimale ;
- documentation ;
- seed demo ;
- tests d'integration ;
- packaging local.

---

## Phase 2 — Pilot Success (EP-007/008/009)

Objectif : transformer RC3 en un produit utilise par un premier pilote. La
reussite n'est plus mesuree par des metriques techniques (tests, packages,
moteurs) mais par les KPIs produit ci-dessous.

### EP-007 — Pilot Success

Objectif : permettre a une entreprise de realiser une premiere session sans
assistance.

- **WP-001 Dashboard pilote ✅** (2026-07-31) : endpoint unique
  `GET /api/v1/pilot/dashboard` — 4 widgets (KPI, entonnoir 6 etapes, activite
  recente, alertes), sans metriques techniques ; alimente par les stores de
  persistance via `PersistenceFactory` (memory en demo, Postgres en prod).
- **WP-002 Error UX ✅** (2026-07-31) : aucun ecran ne montre d'erreur
  "technique" brute. Corps d'erreur backend structure
  (`code/title/explanation/action/retryable/trace_id` + statuts coherents :
  `llm_error`→503, `DATASTORE_UNAVAILABLE`→503, `REPORT_UNAVAILABLE`→503 ;
  handlers globaux Exception/HTTPException/422) ; taxonomy frontend couvrant
  les 8 cas (LLM, STT/TTS, timeout, reseau, scenario introuvable, rapport
  indisponible, PostgreSQL inaccessible, erreur inattendue) ; composants
  `ErrorPanel` + `ErrorBoundary` ; bouton de reprise sur toutes les pages ;
  timeout client 30 s.
- **WP-003 Empty states ✅** (2026-07-31) : aucune page ne paraît "cassée"
  sur une base vide. Composant `EmptyState` uniforme (icone, titre, phrase,
  action principale, lien secondaire) ; 8 vues couvertes — Dashboard (empty
  state au lieu du cockpit a zeros), Mes simulations, Mes rapports, Replay,
  Mes avis, Analytics, Scenarios, Historique vocal ; CTA unique par ecran
  (Commencer une simulation / Lancer une premiere simulation / Ouvrir une
  simulation / Voir le dernier rapport / Decouvrir le tableau de bord) ;
  progressive disclosure (interface complexe revelee seulement avec des
  donnees) ; navigation "Mon activite" en dropdown. Backend : endpoints de
  liste `GET /api/v1/simulations`, `GET /api/v1/reports`,
  `GET /api/v1/voice/sessions` + service `list_sessions` (simulation & voix).
  Bug corrige au passage : `IngestProductEvent` defini en local dans
  `create_app()` rendait `/api/v1/product/events/ingest` en 422 (parametre
  `event` attendu en query) — les events produits par le frontend n'etaient
  jamais ingeres. Modeles de route deplaces au niveau module + `sendBeacon`
  avec content-type `application/json` ; verifie sur memory et PostgreSQL.
- **WP-004 Onboarding polish** (P0) : animations, micro-copy, hierarchie
  visuelle, indicateurs de progression, messages rassurants. Aucune nouvelle
  logique.
- onboarding simplifie ;
- UX des erreurs et des etats vides ;
- documentation d'exploitation.

### EP-010 — Architecture Cleanup (dette planifiee)

Les 12 violations d'architecture et la 1 capability < 50 % sont traitees apres
le premier pilote, sauf si l'une d'elles devient un blocage (fuite
d'abstraction, couplage bloquant EP-007/EP-008, risque de corruption).

### EP-008 — Product Observability

Objectif : comprendre precisement l'usage reel.

- persistance des `ProductEvent` ;
- tableaux de bord internes ;
- entonnoir d'utilisation (Wizard -> Simulation -> Rapport -> Feedback) ;
- indicateurs d'abandon.

### EP-009 — Voice Production Readiness

Objectif : transformer le Voice Runtime en differenciateur commercial.

- **VibeVoice local STT/TTS ✅** (2026-07-31) : parcours voix 100 % local, sans
  cle API ni GPU. STT : VibeASR.cpp (`asr_infer`, inference CPU temps reel sur
  3-4 threads, modeles BitNet quantifies ~1.58 Go — VAE I8_S + LM I2_S).
  TTS : VibeVoice-Realtime-0.5B via son serveur WebSocket (streaming,
  ~200-300 ms premier chunk, PCM16 24 kHz). Adapters
  `VibeVoiceASRAdapter`/`VibeVoiceTTSAdapter` dans le moteur voice (Protocol
  `STTAdapter`/`TTSAdapter` respecte, fallback Mock si non configure).
  Configuration : `CALLIBR_VOICE_STT_PROVIDER` / `CALLIBR_VOICE_TTS_PROVIDER`
  (mock | deepgram | elevenlabs | vibevoice), chemins engine
  `CALLIBR_VIBEVOICE_ASR_*`, URL TTS `CALLIBR_VIBEVOICE_TTS_URL`.
  Verification : 11 tests adapters (CLI stube + serveur WebSocket stube),
  381 tests verts, ruff clean, E2E reelle locale (asr_infer compile, models
  telecharges depuis HF, transcription de parole reelle OK).
- mesure de latence STT/TTS ;
- qualite audio ;
- interruptions (barge-in) ;
- streaming optimise ;
- metriques de satisfaction.

## Tableau de bord KPI — Release 0.1

Metrique principale du pilot : la validation produit par l'usage.

| KPI | Cible Release 0.1 |
| --- | --- |
| Installation reussie | > 95 % |
| Wizard termine | > 90 % |
| Premiere simulation lancee | > 80 % |
| Simulation terminee | > 70 % |
| Rapport consulte | > 60 % |
| Feedback envoye | > 40 % |
| Satisfaction moyenne | >= 4/5 |
| Temps jusqu'a la premiere simulation | < 5 min |

