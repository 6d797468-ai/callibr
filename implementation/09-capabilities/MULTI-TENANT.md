# CAP-15 — Multi-Tenant

Mise a jour : 2026-07-28

## Definition

Capacite d'isoler les donnees et l'acces par tenant : isolation, routage, configuration par tenant.

## Stabilite

Le multi-tenant est un fondamental SaaS. Il ne change pas quand un feature specifique est termine.

## AEB Volumes Concernes

- C03 — Enterprise Multi-Tenant SaaS Architecture

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Tenant Context | `platform/identity/` + middleware API | Actif |
| Tenant ID Propagation | Middleware | Actif |
| Tenant Isolation | Planifie | Planifie |

## Niveaux De Maturite

| Niveau | Description | Statut |
| --- | --- | --- |
| L0 | Tenant ID propage dans les donnees | Actif |
| L1 | Isolation des donnees par tenant | Planifie |
| L2 | Configuration par tenant | Roadmap |
| L3 | Tenant admin dashboard | Roadmap |

## Criteres De Stabilite

Une feature multi-tenant est terminee quand :

- Le tenant ID est present sur toutes les donnees metier
- Les donnees d'un tenant ne sont pas accessibles par un autre
- Les tests couvrent l'isolation de tenant
