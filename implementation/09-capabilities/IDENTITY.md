# CAP-05 — Identity

Mise a jour : 2026-07-28

## Definition

Capacite de gerer les identites utilisateurs, les tenants et le contexte de session authentifie.

## Stabilite

L'identite est un fondamental. Elle ne change pas quand un feature specifique est termine.

## AEB Volumes Concernes

- C03 — Enterprise Multi-Tenant SaaS Architecture
- J01 — IAM & Identity

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Auth Service | `platform/identity/` | Actif |
| User Model | `platform/identity/` | Actif |
| Tenant Context | `platform/identity/` + middleware API | Actif |
| Bearer Token | `platform/identity/` | Actif |

## Contrats

- `POST /auth/login` -> login demo JWT
- Tenant context propage dans toutes les routes metier

## Criteres De Stabilite

Une feature d'identite est terminee quand :

- Un utilisateur peut s'authentifier
- Le tenant context est propage
- Les tests couvrent l'authentification
