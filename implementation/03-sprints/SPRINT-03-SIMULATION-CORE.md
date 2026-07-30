# Sprint 03 — Simulation Core MVP

Mise a jour : 2026-07-28

## Objectif

Construire la premiere tranche verticale exploitable du MVP Callibr.

Cette tranche doit permettre a un apprenant de selectionner un scenario Support/SAV, demarrer une session, dialoguer avec un client simule, executer des actions CRM et recevoir une evaluation initiale.

## Livrables

- contrats API de simulation ;
- catalog scenarios Support/SAV ;
- moteur de simulation texte en memoire ;
- evaluation heuristique initiale ;
- moteur d'actions CRM simulees ;
- endpoints API scenarios, sessions, messages et actions CRM ;
- frontend connecte a la boucle de simulation ;
- tests unitaires et API.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S03-01 | Definir contrats simulation | `ScenarioSummary`, `SimulationSession`, `SimulationMessage` |
| S03-02 | Definir contrats CRM | `CrmActionDefinition`, `CrmActionExecution` |
| S03-03 | Creer catalog SAV | 2 scenarios initiaux |
| S03-04 | Creer simulation service | sessions en memoire |
| S03-05 | Ajouter evaluation initiale | score, forces, risques, prochaines actions |
| S03-06 | Ajouter CRM action simulator | actions eligibles, execution, blocages |
| S03-07 | Exposer API v1 | endpoints scenarios, simulations, CRM |
| S03-08 | Connecter frontend | selection scenario, chat, CRM, score |
| S03-09 | Ajouter tests | API + services |

## Etat D'Execution

Statut : implementation initiale terminee.

## Reste A Durcir

- persistance PostgreSQL des sessions ;
- idempotence des actions CRM ;
- audit trail immutable ;
- scoring multi-criteres ;
- streaming temps reel ;
- orchestration LLM derriere interface stable.

## Definition Of Done

- une session peut etre creee depuis un scenario ;
- un message apprenant produit une reponse client et une evaluation ;
- une action CRM modifie le contexte de session ;
- les actions sensibles sont bloquees si les prerequis ne sont pas respectes ;
- le frontend consomme les endpoints API ;
- tests et build passent.
