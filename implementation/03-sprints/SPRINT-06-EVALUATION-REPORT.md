# Sprint 06 — Detailed Evaluation & Session Report

Mise a jour : 2026-07-28

## Objectif

Transformer le score simple du MVP en premiere evaluation pedagogique exploitable.

Cette tranche ajoute une scorecard detaillee, un moteur d'evaluation dedie, un rapport de session consultable par API et un affichage minimal dans le frontend.

## Livrables

- contrat `EvaluationCriterionResult` ;
- contrat `SessionReport` ;
- champ `criteria` dans `SimulationEvaluation` ;
- champ `completed_at` dans `SimulationSession` ;
- package `callibr_evaluation` ;
- moteur deterministe `EvaluationService` ;
- generation de rapport a partir de la session, des actions CRM et de l'audit trail ;
- endpoint `GET /api/v1/simulations/{session_id}/report` ;
- affichage frontend de la scorecard et du resume de rapport ;
- controle tenant sur les lectures session, audit, actions CRM et rapport ;
- tests API et unitaires.

## Taches

| ID | Tache | Resultat |
| --- | --- | --- |
| S06-01 | Ajouter contrats evaluation | `EvaluationCriterionResult`, `SessionReport` |
| S06-02 | Ajouter Evaluation Engine minimal | `callibr_evaluation.EvaluationService` |
| S06-03 | Brancher SimulationService | evaluation detaillee par criteres |
| S06-04 | Generer rapport session | score, criteres, messages, actions, audit |
| S06-05 | Ajouter endpoint report | `/api/v1/simulations/{session_id}/report` |
| S06-06 | Afficher rapport frontend | scorecard + resume |
| S06-07 | Durcir lecture tenant | session, CRM actions, audit, report |
| S06-08 | Ajouter tests | API + unitaires |

## Scorecard Initiale

Les criteres MVP sont volontairement simples et deterministes :

- empathie ;
- verification client ;
- prise en charge ;
- orientation solution ;
- recapitulatif / prochaine etape.

Chaque critere vaut 20 points. Le score final est normalise sur 100.

## Etat D'Execution

Statut : implementation initiale terminee et validee par tests/lint/build.

## Reste A Durcir

- evaluation multi-tours plutot que dernier tour uniquement ;
- ponderation par scenario et par domain pack ;
- prise en compte explicite des actions CRM dans le score ;
- rapport final verrouille a la cloture de session ;
- persistence dediee des rapports ;
- export PDF/JSON ;
- integration future LLM via gateway stable.

## Definition Of Done

- une session peut produire un rapport via API ;
- le rapport contient score global, criteres, preuves, feedback et recommandations ;
- le frontend affiche la scorecard ;
- les lectures de session/report refusent un tenant different ;
- tests, lint et build passent.
