# CAP-04 — Reporting

Mise a jour : 2026-07-28

## Definition

Capacite de consulter des rapports de session, des statistiques d'agent et des tendances d'apprentissage.

## Stabilite

Le reporting est une capacite transversale. Les metriques evoluent, mais la capacite de rapporter reste.

## AEB Volumes Concernes

- B10 — Analytics, Learning Intelligence & Coaching Platform (ALICP)
- I11-I20 — Data Platform

## Composants (Planifies)

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Session Report | `engines/evaluation/` | Actif (base) |
| Analytics Service | `engines/analytics/` | Planifie |
| Dashboard API | `apps/api/` | Planifie |

## Criteres De Stabilite

Une feature de reporting est terminee quand :

- Un rapport de session est accessible via API
- Les metriques de base sont calculables
- Les tests couvrent la generation de rapport
