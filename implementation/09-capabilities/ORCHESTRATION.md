# CAP-10 — Orchestration

Mise a jour : 2026-07-28

## Definition

Capacite de coordonner les composants de la plateforme : kernel, event bus, command bus et pipeline de traitement.

## Stabilite

L'orchestration est le socle technique. Elle change rarement.

## AEB Volumes Concernes

- C01 — ATOS Kernel
- C02 — Event Bus, Event Sourcing & CQRS

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Kernel | `packages/kernel/` | Actif |
| Command Bus | `packages/kernel/` | Actif |
| Event Bus | `packages/kernel/` | Actif |
| Error Handling | `packages/kernel/` | Actif |
| ID Generation | `packages/kernel/` | Actif |
| Time Provider | `packages/kernel/` | Actif |

## Criteres De Stabilite

Une feature d'orchestration est terminee quand :

- Les commands sont routees correctement
- Les events sont publies et subscribes
- Les erreurs sont standardisees
- Les tests couvrent le kernel
