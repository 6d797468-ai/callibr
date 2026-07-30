# Sprint 04 — Persistence & Audit Trail

Mise a jour : 2026-07-28

## Objectif

Stabiliser l'etat runtime du MVP Callibr avec une couche de persistance injectable et un audit trail append-only.

## Livrables

- package `callibr_persistence` ;
- store de sessions en memoire ;
- store d'audit en memoire ;
- adaptateurs PostgreSQL pour sessions et audit ;
- schema SQL initial ;
- backend de persistance configurable ;
- endpoint d'audit par session ;
- frontend affichant les evenements d'audit ;
- tests unitaires et API.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S04-01 | Definir contrat audit | `AuditRecord` |
| S04-02 | Extraire store session | `SimulationSessionStore` |
| S04-03 | Ajouter store audit | `AuditEventStore` |
| S04-04 | Ajouter adaptateurs memoire | tests rapides sans DB |
| S04-05 | Ajouter adaptateurs PostgreSQL | tables `simulation_sessions`, `audit_events` |
| S04-06 | Brancher `SimulationService` | save/get via store |
| S04-07 | Auditer mutations | session start, message, action CRM |
| S04-08 | Exposer API audit | `/api/v1/simulations/{session_id}/audit` |
| S04-09 | Connecter frontend | panneau Audit |

## Etat D'Execution

Statut : implementation initiale terminee.

## Mode De Persistance

Par defaut :

```bash
CALLIBR_PERSISTENCE_BACKEND=memory
```

Mode PostgreSQL :

```bash
CALLIBR_PERSISTENCE_BACKEND=postgres
CALLIBR_DATABASE_URL=postgresql+psycopg://callibr:callibr@postgres:5432/callibr
```

Le runtime accepte aussi le format psycopg natif `postgresql://`.

## Reste A Durcir

- migrations versionnees ;
- transactions unit-of-work ;
- filtrage audit par tenant ;
- pagination de l'audit ;
- retention et export compliance ;
- tests d'integration PostgreSQL via docker compose.

## Definition Of Done

- une session peut etre sauvegardee et relue depuis un store ;
- les mutations creent des audit records ;
- l'audit est consultable par API ;
- le schema PostgreSQL est fourni ;
- le frontend affiche les evenements d'audit ;
- tests, lint et build passent.
