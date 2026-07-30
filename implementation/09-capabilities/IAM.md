# CAP-06 — IAM

Mise a jour : 2026-07-28

## Definition

Capacite de gerer les roles, permissions et droits d'acces sur les ressources de la plateforme.

## Stabilite

L'IAM evolue de "login local MVP" a "RBAC enterprise", mais la capacite de controler l'acces reste stable.

## AEB Volumes Concernes

- J01 — IAM & Identity
- J02 — RBAC & Access Control
- J03 — Organization & Team Management

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| RBAC Minimal | `platform/identity/` | MVP (roles agent/admin) |
| Role Manager | `platform/identity/` | Planifie |
| Permission Engine | `platform/identity/` | Planifie |

## Niveaux De Maturite

| Niveau | Description | Statut |
| --- | --- | --- |
| L0 | Login local JWT | Actif |
| L1 | Roles agent/admin | Actif |
| L2 | Permissions par ressource | Planifie |
| L3 | RBAC enterprise complet | Roadmap |

## Criteres De Stabilite

Une feature IAM est terminee quand :

- Les roles sont verifies sur les routes protegees
- Les permissions bloquent l'acces non autorise
- Les tests couvrent les cas d'acces
