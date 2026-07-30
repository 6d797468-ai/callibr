# Volume L04 — Product Metrics, OKR & Outcome Measurement Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE L — PRODUCT GOVERNANCE, ARCHITECTURE GOVERNANCE & ENTERPRISE OPERATIONS
Volume L04
Product Metrics, OKR & Outcome Measurement Architecture

Version : 1.0

Statut : Enterprise Outcome Foundation

Criticité : Critique

1. Vision

Les Product Metrics mesurent si Callibr crée réellement de la valeur.

Elles relient :

usage ;
activation ;
adoption ;
rétention ;
qualité ;
revenu ;
coût ;
satisfaction ;
risque.

2. Principe fondamental

Ce qui n'est pas mesuré devient opinion.

Ce qui est mal mesuré devient dangereux.

3. Architecture globale

                    Product Events


                         │


                         ▼


                    Metrics Framework


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


 North Star        OKR Metrics       Health Metrics

4. Metric Taxonomy

Familles :

acquisition ;
activation ;
engagement ;
adoption ;
retention ;
expansion ;
quality ;
reliability ;
unit economics ;
customer outcomes.

5. North Star Metric

Recommandation Callibr :

Nombre de simulations qualifiantes complétées avec amélioration mesurable de compétence.

Cette métrique combine :

usage ;
qualité ;
apprentissage ;
valeur client.

6. OKR Model

Chaque objectif possède :

objective ;
key results ;
owner ;
baseline ;
target ;
period ;
confidence ;
status.

7. Metric Guardrails

Contre-métriques :

coût IA ;
latence ;
support tickets ;
guardrail blocks ;
churn risk ;
quality regression ;
user frustration.

8. Experiment Metrics

Chaque expérimentation définit :

hypothesis ;
primary metric ;
guardrail metrics ;
sample ;
duration ;
decision rule.

9. Data Model

ProductMetric
-------------

id

name

definition

owner

source

status

OKR
---

id

objective

owner

period

status

KeyResult
---------

id

okr_id

metric_id

baseline

target

current_value

10. API interne

Créer métrique :

POST /product-metrics/metrics

Créer OKR :

POST /product-metrics/okrs

Lire scorecard :

GET /product-metrics/scorecards/{portfolio}

11. Décisions d'architecture (ADR)

ADR-L04-001
Les métriques produit ont un owner.

Décision :

Garantir qualité et interprétation.

ADR-L04-002
Les OKR sont liés aux métriques gouvernées.

Décision :

Éviter les objectifs non mesurables.

ADR-L04-003
Chaque métrique critique a des guardrails.

Décision :

Empêcher l'optimisation locale dangereuse.

ADR-L04-004
Les expérimentations ont des règles de décision.

Décision :

Réduire biais et décisions opportunistes.

12. Critères d'acceptation

Product Metrics conforme lorsque :

les métriques sont définies ;
les sources sont traçables ;
les OKR ont baseline et target ;
les guardrails existent ;
les expérimentations ont décision ;
les dashboards utilisent des métriques gouvernées.

Décision majeure : Measured Product Outcomes

Callibr mesure la valeur produit par résultats, pas par volume de fonctionnalités.
