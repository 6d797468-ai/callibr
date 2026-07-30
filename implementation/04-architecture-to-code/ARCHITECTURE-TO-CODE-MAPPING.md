# Architecture To Code Mapping

Mise a jour : 2026-07-27

## Mapping Principal

| Concept AEB | Emplacement cible | Sprint initial |
| --- | --- | --- |
| Kernel | `packages/kernel` | S01 |
| Contracts | `packages/contracts` | S01 |
| Identity | `platform/identity` | S02 |
| Tenant Context | `platform/identity` + middleware API | S02 |
| Simulation Engine | `engines/simulation` | S03 |
| Conversation Engine | `engines/conversation` | S03 |
| Scenario Engine | `engines/scenario` | S04 |
| Persona Engine | `engines/persona` | S04 |
| CRM Runtime | `engines/crm` | S05 |
| Action Engine | `engines/crm/application/actions` | S06 |
| Procedure Engine | `engines/procedure` | S07 |
| Evaluation Engine | `engines/evaluation` | S08 |
| Support SAV Domain Pack | `domains/support_sav` | S04 |
| API | `apps/api` | S00 |
| Frontend | `apps/frontend` | S00 |
| PostgreSQL | `infrastructure/postgres` | S00 |
| Redis | `infrastructure/redis` | S00 |

## Contrats MVP

| Contrat | Type | Usage |
| --- | --- | --- |
| `StartSimulationCommand` | command | lancer une session |
| `SendMessageCommand` | command | envoyer message agent |
| `RunCrmActionCommand` | command | executer action CRM |
| `EndSimulationCommand` | command | terminer session |
| `SimulationStarted` | event | timeline/session |
| `MessageAdded` | event | conversation |
| `CrmActionExecuted` | event | audit metier |
| `SimulationCompleted` | event | evaluation |
| `EvaluationGenerated` | event | reporting |

## API MVP

| Endpoint | But | Sprint |
| --- | --- | --- |
| `GET /health` | healthcheck | S00 |
| `POST /auth/login` | login demo | S02 |
| `GET /scenarios` | lister scenarios | S04 |
| `POST /simulations` | lancer session | S03 |
| `GET /simulations/{id}` | lire session | S03 |
| `POST /simulations/{id}/messages` | envoyer message | S03 |
| `POST /simulations/{id}/crm/actions` | action CRM | S06 |
| `POST /simulations/{id}/end` | terminer | S08 |
| `GET /simulations/{id}/evaluation` | rapport QA | S08 |

