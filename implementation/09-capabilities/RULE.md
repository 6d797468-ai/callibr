# CAP-13 — Rule & Decision

Mise a jour : 2026-07-28

## Definition

Capacite d'evaluer des regles metier simples et de prendre des decisions basees sur ces regles pendant la simulation.

## Stabilite

La capacite d'evaluer des regles est stable. Les regles specifiques changent.

## AEB Volumes Concernes

- B06 — Rule Engine & Decision Engine

## Composants (Planifies)

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Rule Engine | `engines/rule/` | Planifie |
| Decision Engine | `engines/rule/` | Planifie |

## Criteres De Stabilite

Une feature rule est terminee quand :

- Des regles peuvent etre definies et evaluees
- Les decisions sont prises sur la base des regles
- Les tests couvrent l'evaluation de regles
