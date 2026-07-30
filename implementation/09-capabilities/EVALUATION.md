# CAP-03 — Evaluation

Mise a jour : 2026-07-28

## Definition

Capacite de produire un score QA base sur une grille d'evaluation, de generar des feedbacks textuels et de calculer un score final de session.

## Stabilite

L'evaluation est un pilier de la valeur produit. La grille evolue, mais la capacite d'evaluer reste.

## AEB Volumes Concernes

- B09 — Evaluation & Quality Intelligence Engine (EQI)

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Evaluation Engine | `engines/evaluation/` | Actif |
| Scorecard | `engines/evaluation/` | Actif |
| Feedback Generator | `engines/evaluation/` | Actif |
| Session Report | `engines/evaluation/` | Actif |

## Contrats

- `EvaluationGenerated` -> evenement evaluation produite

## Criteres De Stabilite

Une feature d'evaluation est terminee quand :

- Un score QA est produit a la fin d'une session
- Un feedback textuel est genere
- Un rapport de session est consultable
- Les tests couvrent le calcul de score
