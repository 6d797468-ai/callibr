# Epic Backlog

Mise a jour : 2026-07-27

## Priorite P0 — Bootstrap

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-000 | Monorepo bootstrap | structure creee, README, tooling |
| EPIC-001 | Backend API shell | FastAPI demarre, healthcheck |
| EPIC-002 | Frontend shell | page de base demarre |
| EPIC-003 | Local runtime | docker compose avec db/cache |
| EPIC-004 | Tooling qualite | ruff, pytest, typing baseline |

## Priorite P1 — Platform Core

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-010 | Kernel minimal | config, ids, time, errors |
| EPIC-011 | Command bus | handler commands synchrones |
| EPIC-012 | Event bus local | publish/subscribe in-process |
| EPIC-013 | Persistence | SQLAlchemy, Alembic, repositories |
| EPIC-014 | Tenant context | tenant_id propage dans API/domain |

## Priorite P2 — Identity

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-020 | Auth demo | login local JWT |
| EPIC-021 | Users | model utilisateur |
| EPIC-022 | RBAC minimal | roles agent/admin |
| EPIC-023 | Tenant membership | user rattache a tenant |

## Priorite P3 — Simulation

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-030 | Simulation session | start/end session |
| EPIC-031 | Conversation timeline | messages persistants |
| EPIC-032 | Scenario catalog | scenarios SAV seedes |
| EPIC-033 | Persona runtime | comportement client simple |
| EPIC-034 | LLM provider port | stub puis adapter |

## Priorite P4 — CRM Simulator

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-040 | Customer model | client fictif |
| EPIC-041 | Search customer | recherche CRM |
| EPIC-042 | Verify identity | verification deterministe |
| EPIC-043 | Ticket model | creation ticket |
| EPIC-044 | CRM event trail | journal des actions |

## Priorite P5 — Procedure & Rules

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-050 | Procedure checklist | etapes scenario |
| EPIC-051 | Rule evaluation | regles simples |
| EPIC-052 | Objective tracking | objectifs session |
| EPIC-053 | Failure detection | erreurs procedure |

## Priorite P6 — Evaluation & Learning

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-060 | QA scorecard | grille simple |
| EPIC-061 | Evaluation engine | score final |
| EPIC-062 | Feedback generator | conseils textuels |
| EPIC-063 | Report view | rapport session |

## Priorite P7 — Operations MVP

| Epic | Objectif | Done |
| --- | --- | --- |
| EPIC-070 | Structured logs | logs JSON |
| EPIC-071 | Metrics baseline | compteurs API/sessions |
| EPIC-072 | Test suite | unit + integration |
| EPIC-073 | Demo seed | donnees demo reproductibles |
| EPIC-074 | MVP docs | runbook local |

