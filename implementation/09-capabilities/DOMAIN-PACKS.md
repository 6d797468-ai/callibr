# CAP-17 — Domain Packs

Mise a jour : 2026-07-28

## Definition

Capacite de charger des packs de domaines specifiques : scenarios, personas, procedures et regles pour un metier donne (SAV, support, telesales, etc.).

## Stabilite

Les domain packs sont un concept stable. Les packs specifiques changent, mais la capacite de les charger reste.

## AEB Volumes Concernes

- G00-G20 — Contact Center Packs

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Support/SAV Pack | `domains/support_sav/` | Actif (seed) |
| Domain Pack Registry | Planifie | Planifie |
| Domain Pack Loader | Planifie | Planifie |

## Packs Planifies

| Pack | Statut |
| --- | --- |
| Support Client / SAV | Actif (2 scenarios) |
| Telesales | Roadmap |
| Retention | Roadmap |
| Technical Support | Roadmap |
| Debt Collection | Roadmap |

## Criteres De Stabilite

Une feature domain pack est terminee quand :

- Un pack peut etre charge dynamiquement
- Les scenarios et personas du pack sont disponibles
- Les tests couvrent le chargement de pack
