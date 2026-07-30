# Sprint 00 — Bootstrap

Mise a jour : 2026-07-27

## Objectif

Creer les fondations techniques minimales pour demarrer le developpement Callibr.

## Livrables

- structure monorepo ;
- backend FastAPI minimal ;
- frontend minimal ;
- docker compose ;
- PostgreSQL ;
- Redis ;
- configuration locale ;
- tests de smoke ;
- README developpeur.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S00-01 | Creer arborescence cible | dossiers `apps`, `packages`, `services`, `engines`, `platform` |
| S00-02 | Initialiser backend API | healthcheck `/health` |
| S00-03 | Initialiser frontend | page shell Callibr |
| S00-04 | Ajouter docker compose | API, frontend, postgres, redis |
| S00-05 | Ajouter config env | `.env.example` |
| S00-06 | Ajouter tests smoke | API health test |
| S00-07 | Ajouter tooling Python | ruff, pytest, pyproject |
| S00-08 | Documentation bootstrap | commandes locales |

## Definition Of Done

- `docker compose up` demarre.
- API repond sur `/health`.
- Frontend affiche une page.
- Tests smoke passent.
- README explique les commandes.

## Risques

- surdimensionner trop tot ;
- choisir un outillage qui ralentit ;
- melanger docs et code sans convention.

## Decision

Le Sprint 00 doit rester volontairement petit.

Pas de domaine metier avant que le runtime local soit stable.

