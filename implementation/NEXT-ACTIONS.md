# Next Actions

Mise a jour : 2026-07-28

## Action 1 — Valider Le Mode De Demarrage

Decision recommandee :

Demarrer par un monorepo applicatif dans ce workspace, avec backend FastAPI et frontend minimal.

Statut : termine.

## Action 2 — Creer Le Squelette Repo

Creer :

- `apps/api`
- `apps/frontend`
- `packages/kernel`
- `packages/contracts`
- `packages/shared`
- `platform/identity`
- `engines/simulation`
- `engines/conversation`
- `engines/scenario`
- `engines/persona`
- `engines/crm`
- `engines/evaluation`
- `domains/support_sav`
- `tests`
- `deployments/local`

Statut : termine.

## Action 3 — Initialiser Tooling Backend

Ajouter :

- `pyproject.toml`
- FastAPI ;
- Pydantic ;
- pytest ;
- ruff ;
- settings ;
- healthcheck.

Statut : termine.

## Action 4 — Initialiser Runtime Local

Ajouter :

- `docker-compose.yml`
- PostgreSQL ;
- Redis ;
- variables `.env.example`.

Statut : termine.

## Action 5 — Initialiser Frontend

Creer une premiere interface :

- shell Callibr ;
- route home ;
- placeholder liste scenarios ;
- placeholder simulation.

Statut : termine. Le shell est maintenant branche sur les endpoints de simulation.

## Action 6 — Premier Test De Bout En Bout

Valider :

1. API demarre.
2. Frontend demarre.
3. `/health` repond.
4. test smoke passe.

Statut : partiellement termine. API et tests Python valides ; build frontend a verifier apres installation npm.

## Definition Du Prochain Resultat Visible

Le prochain resultat visible doit etre :

Une simulation SAV complete lancee depuis le frontend, avec session, messages, contexte CRM et score initial.

## Action 7 — Tranche Verticale Simulation SAV

Ajouter :

- contrats API `ScenarioSummary`, `SimulationSession`, `SimulationMessage` ;
- catalog scenarios Support/SAV ;
- moteur de simulation texte en memoire ;
- endpoints `/api/v1/scenarios` et `/api/v1/simulations` ;
- tests API et unitaires.

Statut : en cours.

## Action 8 — CRM Action Simulator

Ajouter :

- contrats d'actions CRM ;
- moteur `callibr_crm` ;
- actions `verification_identite`, `consultation_suivi_colis`, `creation_ticket_transporteur`, `notification_client` ;
- actions facturation pour le second scenario SAV ;
- endpoint de listing des actions ;
- endpoint d'execution d'action ;
- affichage et execution depuis le panneau CRM frontend ;
- tests de blocage metier.

Statut : termine pour l'implementation initiale.

## Prochaine Action Recommandee

Introduire le Procedure Engine MVP et ajouter les tests d'integration PostgreSQL.

## Action 9 — Persistence & Audit Trail

Ajouter :

- contrat `AuditRecord` ;
- package `callibr_persistence` ;
- stores memoire pour tests et dev local ;
- adaptateurs PostgreSQL pour sessions et audit ;
- schema SQL initial ;
- endpoint `/api/v1/simulations/{session_id}/audit` ;
- affichage audit dans le frontend.

Statut : termine pour l'implementation initiale.

## Action 10 — Local IAM MVP

Ajouter :

- contrats auth ;
- hash mot de passe ;
- token bearer signe ;
- store identite memoire/PostgreSQL ;
- seed utilisateur demo ;
- endpoint `/api/v1/auth/login` ;
- contexte tenant/user depuis bearer token ;
- frontend connecte au login demo.

Statut : termine pour l'implementation initiale.

## Action 11 — Detailed Evaluation & Session Report

Ajouter :

- contrats `EvaluationCriterionResult` et `SessionReport` ;
- moteur `callibr_evaluation` ;
- scorecard par criteres ;
- endpoint `/api/v1/simulations/{session_id}/report` ;
- affichage scorecard et rapport dans le frontend ;
- controle tenant sur les lectures de session, CRM actions, audit et rapport ;
- tests API et unitaires.

Statut : termine pour l'implementation initiale.

## Action 12 — Procedure Engine MVP & Conversation Runtime

Ajouter :

- contrat de procedure ✓ ;
- checklist par scenario ✓ ;
- etat d'avancement procedure dans la session ✓ ;
- integration avec actions CRM ✓ ;
- affichage frontend ✓ ;
- evaluation des obligations procedurelles ✓.

Inclus dans S12 :

- module `callibr_seed` : 2 personas, 2 procedures, 2 regles, 2 scenarios charges au demarrage ✓ ;
- `ProcedureExecutor` auto-advance par `order` ✓ ;
- `TraitName` elargi aux traits client ✓ ;
- `ProcedureService._append_audit` corrige (AuditRecord reel) ✓ ;
- 18 nouveaux tests ✓ ;
- bugfixes gate : APIRouter, tenant fallback, imports lifespan ✓.

Statut : **termine**.

## Prochaine Action Recommandee

Introduire S13 : integration `SimulationService` ↔ `ConversationService` et activation PostgreSQL.

## Action 13 — Integration SimulationService ↔ ConversationService

Objectif : brancher le moteur de simulation existant sur le `ConversationService` pour que le parcours utilisateur soit unique, et activer PostgreSQL comme backend par defaut.

Ajouter :

- passerelle `SimulationService.start_session()` → `ConversationService.start_conversation()` ;
- propagation du `execution_id` de procedure dans la session de simulation ;
- activation PostgreSQL (`PERSISTENCE_BACKEND=postgres`) et migrations Alembic initiales ;
- tests d'integration smoke PostgreSQL via `docker-compose` ;
- rapport de session incluant la progression procedurale.

Statut : prochaine action recommandee.

