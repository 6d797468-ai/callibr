# CAP-08 — Scenario

Mise a jour : 2026-07-28

## Definition

Capacite de definir, stocker et charger des scenarios de simulation : contexte, objectifs, persona client, etapes et regles.

## Stabilite

Le scenario est un concept fondamental. La structure evolue, mais la capacite de charger un scenario reste.

## AEB Volumes Concernes

- B05 — Scenario Engine & Procedure Engine

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Scenario Catalog | `engines/scenario/` | Actif (seed data) |
| Scenario Loader | `engines/scenario/` | Actif |
| Domain Pack Scenarios | `domains/support_sav/` | Actif (2 scenarios) |

## Contrats

- `GET /scenarios` -> lister les scenarios disponibles

## Criteres De Stabilite

Une feature scenario est terminee quand :

- Un scenario peut etre charge depuis le catalogue
- Le contexte et les objectifs sont exposes a la simulation
- Les tests couvrent le chargement de scenario
