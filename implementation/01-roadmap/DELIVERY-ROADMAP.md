# Delivery Roadmap

Mise a jour : 2026-07-27

Cadence recommandee : sprint de 2 semaines.

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

