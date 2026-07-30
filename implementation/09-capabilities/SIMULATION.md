# CAP-01 — Simulation

Mise a jour : 2026-07-28

## Definition

Capacite de lancer, mener et terminer une session de simulation textuelle entre un agent en formation et un client simule.

## Stabilite

Cette capability est fondamentale. Elle ne change pas quand un epic est termine.

Elle supporte les epics suivants :

- EPIC-030 : Simulation session (start/end)
- EPIC-031 : Conversation timeline
- EPIC-034 : LLM provider port
- Futurs epics : simulation avancee, multi-tour, voice

## AEB Volumes Concernes

- B02 — Simulation Operating Engine (SOE)
- B08 — Conversation Runtime Engine (CoRE)
- C01 — ATOS Kernel

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Simulation Service | `engines/simulation/` | Actif |
| Conversation Engine | `engines/conversation/` | Planifie |
| Session Manager | `engines/simulation/` | Actif |
| Message Store | `engines/simulation/` | Actif |

## Contrats

- `StartSimulationCommand` -> lance une session
- `SendMessageCommand` -> envoie un message agent
- `EndSimulationCommand` -> termine la session
- `SimulationStarted` -> evenement debut
- `MessageAdded` -> evenement message
- `SimulationCompleted` -> evenement fin

## Criteres De Stabilite

Une feature de simulation est terminee quand :

- Une session peut etre demarree, menee et terminee
- Les messages sont persistes
- Les evenements sont emis
- Le tout est couvert par des tests
