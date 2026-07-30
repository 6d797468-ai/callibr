# Sprint 05 — Local IAM MVP

Mise a jour : 2026-07-28

## Objectif

Transformer l'identite demo en flux IAM local utilisable par le MVP.

Cette tranche apporte un login local, un token bearer signe, un store d'identite injectable et la compatibilite avec le contexte tenant/user existant.

## Livrables

- contrats `LoginRequest`, `AuthToken`, `IdentityUserRecord` ;
- hash de mot de passe PBKDF2 ;
- token signe HMAC avec expiration ;
- store identite en memoire ;
- adaptateur PostgreSQL pour tenants et users ;
- seed utilisateur demo ;
- endpoint `POST /api/v1/auth/login` ;
- endpoint `/api/v1/me` compatible bearer token ;
- frontend connecte au login demo ;
- tests API et unitaires.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S05-01 | Ajouter contrats auth | `LoginRequest`, `AuthToken` |
| S05-02 | Ajouter user record | `IdentityUserRecord` |
| S05-03 | Ajouter password hashing | PBKDF2 SHA-256 |
| S05-04 | Ajouter token signing | HMAC HS256 |
| S05-05 | Ajouter identity store | memoire + PostgreSQL |
| S05-06 | Seed demo user | `learner@demo.callibr.local` |
| S05-07 | Ajouter login API | `/api/v1/auth/login` |
| S05-08 | Ajouter bearer context | `Authorization: Bearer` |
| S05-09 | Connecter frontend | login demo automatique |

## Identifiants Demo

```text
tenant_id: tenant_demo
email: learner@demo.callibr.local
password: callibr-demo
```

## Etat D'Execution

Statut : implementation initiale terminee.

## Reste A Durcir

- rotation des secrets ;
- refresh tokens ;
- expiration/revocation serveur ;
- roles et permissions par policy ;
- verification stricte tenant/session ;
- ecrans login/logout ;
- tests d'integration PostgreSQL.

## Definition Of Done

- un utilisateur demo peut obtenir un token ;
- `/api/v1/me` accepte le bearer token ;
- les simulations utilisent le tenant/user du token ;
- un mauvais mot de passe retourne `401` ;
- les stores identite sont injectables ;
- tests, lint et build passent.
