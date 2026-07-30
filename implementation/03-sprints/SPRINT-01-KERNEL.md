# Sprint 01 — Kernel Minimal

Mise a jour : 2026-07-27

## Objectif

Construire le noyau minimal permettant aux futurs engines de communiquer proprement.

## Livrables

- config service ;
- ID/time utilities ;
- error model ;
- command bus synchrone ;
- event bus in-process ;
- structured logging ;
- contrats de base.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S01-01 | Creer package kernel | module importable |
| S01-02 | Config runtime | settings Pydantic |
| S01-03 | Command bus | register + dispatch |
| S01-04 | Event bus local | publish + handlers |
| S01-05 | Error model | erreurs standardisees |
| S01-06 | Logging | trace_id, tenant_id |
| S01-07 | Tests unitaires | command/event bus couverts |

## Etat D'Execution

Statut : implementation initiale terminee.

Livres :

- package `callibr_kernel` ;
- package `callibr_telemetry` ;
- command bus synchrone ;
- event bus in-process ;
- modeles d'erreurs ;
- utilitaires ID/time ;
- tests kernel et telemetry.

Reste a durcir :

- correlation automatique des logs depuis middleware API ;
- propagation systematique du `trace_id` dans les commandes et events ;
- contrats d'observabilite OpenTelemetry.

## Definition Of Done

- un handler de command peut etre enregistre et execute ;
- un event peut etre publie et consomme ;
- les logs incluent trace_id ;
- les tests kernel passent.
