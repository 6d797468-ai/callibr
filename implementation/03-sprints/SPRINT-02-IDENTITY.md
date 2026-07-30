# Sprint 02 — Identity & Tenant Context

Mise a jour : 2026-07-28

## Objectif

Introduire l'identite minimale et le contexte tenant afin que tous les developpements suivants soient multi-tenant par conception.

## Livrables

- tenant demo ;
- user demo ;
- contexte tenant par headers ;
- trace id par requete ;
- endpoint `/api/v1/me` ;
- roles `agent` et `learner` ;
- provider d'identite demo.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S02-01 | Model Tenant | contrat `TenantInfo` |
| S02-02 | Model User | contrat `AuthenticatedUser` |
| S02-03 | Membership | rattachement tenant/user via contexte |
| S02-04 | Login local | reporte apres persistance |
| S02-05 | Tenant middleware | `X-Tenant-Id`, `X-User-Id`, `X-Trace-Id` |
| S02-06 | RBAC minimal | roles demo `agent`, `learner` |
| S02-07 | Seed demo | provider demo |

## Etat D'Execution

Statut : implementation demo terminee.

Livre :

- package `callibr_identity` ;
- contrats `AuthenticatedUser` et `TenantInfo` ;
- endpoint `/api/v1/me` ;
- propagation `tenant_id`, `user_id`, `trace_id` ;
- override du tenant et learner sur creation de simulation ;
- header de reponse `X-Trace-Id` ;
- tests API et unitaires.

Reste a durcir :

- login local ;
- JWT ;
- stockage PostgreSQL des tenants, users et memberships ;
- RBAC par policy ;
- seed demo persistant.

## Definition Of Done

- une requete porte un `tenant_id` ;
- une requete porte un `user_id` ;
- une requete porte un `trace_id` ;
- `/api/v1/me` retourne l'utilisateur courant ;
- les tests d'identite passent.
