# Volume I14 — Feature Store & ML Data Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I14
Feature Store & ML Data Platform Architecture

Version : 1.0

Statut : Enterprise ML Data Foundation

Criticité : Élevée

1. Vision

Le Feature Store fournit les variables utilisées par les modèles d'IA, les modèles prédictifs et les moteurs d'aide à la décision.

Il sert notamment :

prédiction de churn ;
recommandation de coaching ;
détection d'anomalies ;
routage modèle ;
score de compétence ;
prévision WFM ;
optimisation coûts IA.

2. Principe fondamental

Une feature doit être définie une seule fois et utilisée partout de façon cohérente.

Sans Feature Store :

chaque équipe recalcule ses variables.

Avec Feature Store :

feature contract

↓

offline computation

↓

online serving

↓

monitoring

3. Architecture globale

                    Raw / Curated Data


                           │


                           ▼


                    Feature Pipelines


                           │


          ┌────────────────┼────────────────┐


          ▼                ▼                ▼


 Offline Store      Online Store      Feature Registry


          │                │                │


          ▼                ▼                ▼


 Training Jobs      Real-time Inference   Monitoring

4. Feature Types

Types :

agent features ;
session features ;
scenario features ;
tenant features ;
conversation features ;
QA features ;
WFM features ;
AI cost features ;
security features.

5. Feature Contract

Exemple :

feature:
  name: agent_empathy_rolling_score_30d
  entity: agent
  type: float
  window: 30d
  owner: learning_ai
  freshness: 24h
  classification: internal

6. Offline Store

Utilisé pour :

entraînement ;
backtesting ;
analyse historique ;
benchmark ;
recalibrage.

Stockage recommandé :

Lakehouse / Warehouse.

7. Online Store

Utilisé pour :

inférence temps réel ;
recommandations ;
alertes ;
routage ;
coaching pendant session.

Technologies possibles :

Redis ;
Cassandra ;
DynamoDB ;
PostgreSQL optimisé ;
vector store hybride.

8. Point-in-Time Correctness

Les features d'entraînement doivent respecter le temps.

Interdiction :

utiliser une donnée future pour prédire un événement passé.

Le Feature Store doit fournir des joins temporels corrects.

9. Feature Freshness

Niveaux :

real time ;
minutes ;
horaire ;
quotidien ;
hebdomadaire.

Chaque feature déclare sa fraîcheur attendue.

10. Drift Monitoring

Surveillance :

distribution ;
valeurs manquantes ;
outliers ;
stabilité ;
corrélation ;
impact modèle.

11. Training Dataset Generation

Le système génère :

dataset ;
labels ;
features ;
time range ;
sampling ;
metadata ;
lineage.

12. Feature Governance

Une feature possède :

owner ;
description ;
contrat ;
classification ;
validations ;
consommateurs ;
statut.

13. Data Model

FeatureDefinition
-----------------

id

name

entity

value_type

owner

freshness

status

FeatureValue
------------

feature_id

entity_id

timestamp

value

TrainingDataset
---------------

id

name

feature_set

label

time_range

version

14. API interne

Lire feature :

GET /features/{name}/entities/{entity_id}

Créer feature :

POST /features

Générer dataset :

POST /features/datasets

15. Décisions d'architecture (ADR)

ADR-I14-001
Les features IA sont gouvernées.

Décision :

Éviter les variables implicites et non documentées.

ADR-I14-002
Offline et online stores sont séparés.

Décision :

Optimiser entraînement et inférence.

ADR-I14-003
La correction temporelle est obligatoire.

Décision :

Éviter les modèles surévalués par fuite de données.

ADR-I14-004
Le drift est surveillé.

Décision :

Détecter la dégradation progressive des modèles.

16. Critères d'acceptation

Feature Store conforme lorsque :

les features sont cataloguées ;
les valeurs offline et online sont cohérentes ;
les datasets d'entraînement sont reproductibles ;
la correction temporelle est garantie ;
le drift est mesuré ;
les usages sont traçables.

Décision majeure : Governed ML Features

Les features deviennent des actifs de plateforme, pas des transformations cachées dans des notebooks.
