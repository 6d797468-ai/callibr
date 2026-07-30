# CAP-11 — Procedure

Mise a jour : 2026-07-28

## Definition

Capacite de valider les etapes d'une procedure metier pendant la simulation : checklist, verification, detection d'erreurs.

## Stabilite

La procedure est un concept stable. Les procedures specifiques changent, mais la capacite de valider reste.

## AEB Volumes Concernes

- B05 — Scenario Engine & Procedure Engine
- B06 — Rule Engine & Decision Engine

## Composants (Planifies)

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Procedure Engine | `engines/procedure/` | Planifie |
| Procedure Checklist | `engines/procedure/` | Planifie |
| Objective Tracking | `engines/procedure/` | Planifie |
| Failure Detection | `engines/procedure/` | Planifie |

## Criteres De Stabilite

Une feature procedure est terminee quand :

- Une checklist de procedure est chargee
- Les etapes sont validees une par une
- Les erreurs sont detectees et signalees
- Les tests couvrent la validation de procedure
