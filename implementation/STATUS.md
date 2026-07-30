# Implementation Status

Mise a jour : 2026-07-28

## Etat Courant

Callibr est passe de la phase documentaire a une premiere tranche executable.

## Termine

- monorepo initialise ;
- backend FastAPI minimal ;
- frontend Vite/React minimal ;
- docker compose local ;
- contexte tenant/user demo ;
- endpoint identite `/api/v1/me` ;
- endpoint login `/api/v1/auth/login` ;
- token bearer signe pour le MVP ;
- hash mot de passe PBKDF2 ;
- stores identite memoire/PostgreSQL ;
- propagation `X-Trace-Id` ;
- contrats API de simulation ;
- contrat d'audit `AuditRecord` ;
- package de persistance `callibr_persistence` ;
- kernel minimal : erreurs, ID, temps, command bus, event bus ;
- journalisation structuree avec `trace_id` et `tenant_id` ;
- scenario catalog en memoire pour le Domain Pack Support/SAV ;
- moteur de simulation texte en memoire ;
- moteur d'actions CRM simulees ;
- endpoints API scenarios et simulations ;
- endpoints API actions CRM ;
- endpoint API audit par session ;
- endpoint API rapport de session ;
- connexion frontend/API sur la boucle de simulation ;
- execution d'actions CRM depuis le frontend ;
- affichage audit dans le frontend ;
- affichage scorecard et resume de rapport dans le frontend ;
- login demo automatique dans le frontend ;
- schema PostgreSQL initial pour sessions et audit ;
- schema PostgreSQL initial pour tenants et users ;
- moteur d'evaluation detaillee `callibr_evaluation` ;
- scorecard MVP par criteres ;
- contrat `SessionReport` ;
- controle tenant sur les lectures session, CRM actions, audit et rapport ;
- tests API et unitaires.

## En Cours

- durcissement de la premiere tranche verticale MVP ;
- preparation du Procedure Engine MVP ;
- preparation des tests d'integration PostgreSQL.

## Prochaines Etapes

1. Introduire le Procedure Engine MVP.
2. Ajouter les tests d'integration PostgreSQL via docker compose.
3. Prendre en compte les actions CRM dans le score final.
4. Ajouter roles et permissions par policy.
5. Preparer le moteur LLM derriere une interface stable.
