# Volume I13 — Lakehouse, Warehouse & Data Product Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I13
Lakehouse, Warehouse & Data Product Architecture

Version : 1.0

Statut : Enterprise Data Storage Foundation

Criticité : Critique

1. Vision

Le Lakehouse et le Warehouse stockent les données historiques, analytiques et semi-structurées de Callibr.

Ils permettent :

historisation longue ;
analyse BI ;
entraînement modèles ;
reporting ;
audit ;
exports clients ;
data products.

2. Principe fondamental

Les bases applicatives ne sont pas le système analytique.

Elles servent les transactions.

Le Lakehouse et le Warehouse servent l'analyse, le recalcul et l'exploitation longue durée.

3. Architecture globale

                    Data Sources


                         │


                         ▼


                    Ingestion Layer


                         │


       ┌─────────────────┼─────────────────┐


       ▼                 ▼                 ▼


   Raw Zone         Curated Zone        Warehouse


       │                 │                 │


       ▼                 ▼                 ▼


 Data Products     ML Datasets        BI / Reporting

4. Storage Zones

Raw Zone

Données brutes, immuables, contrôlées.

Curated Zone

Données nettoyées et normalisées.

Serving Zone

Données prêtes pour BI, API et ML.

5. Data Product Model

Un data product possède :

owner ;
contrat ;
schéma ;
SLA ;
qualité ;
documentation ;
permissions ;
cycle de vie.

Exemples :

ConversationQualityDataset ;
AgentProgressMart ;
TenantUsageMart ;
AIUsageCostDataset.

6. Warehouse Modeling

Modèles :

facts ;
dimensions ;
snapshots ;
slowly changing dimensions ;
aggregates.

Exemples :

fact_simulation ;
fact_conversation_turn ;
fact_evaluation_score ;
dim_agent ;
dim_scenario ;
dim_tenant.

7. Lakehouse Formats

Formats recommandés :

Parquet ;
Delta Lake ;
Apache Iceberg ;
Apache Hudi.

Le choix doit supporter versioning, partitioning et schema evolution.

8. Partitioning

Partitions principales :

tenant_id ;
date ;
event_type ;
domain_pack ;
region.

Objectif :

réduire coût et temps de lecture.

9. Data Retention

Chaque dataset déclare :

durée ;
archive ;
purge ;
résidence ;
classification ;
base légale.

10. Data Product Registry

Le registry référence :

nom ;
owner ;
description ;
schéma ;
qualité ;
SLA ;
lineage ;
consommateurs.

11. Transformation Layer

Transformations :

normalisation ;
join ;
enrichissement ;
anonymisation ;
agrégation ;
validation ;
publication.

Les transformations sont versionnées.

12. Data Serving

Modes :

SQL ;
API ;
BI connector ;
notebook ;
ML pipeline ;
export contrôlé.

13. Cost Management

La Data Platform suit :

stockage ;
requêtes ;
transferts ;
compute ;
exports ;
coût par tenant ;
coût par data product.

14. Data Model

DataProduct
-----------

id

name

owner

domain

schema_ref

sla

classification

DatasetVersion
--------------

id

data_product_id

version

storage_path

created_at

DataPartition
-------------

id

dataset_version_id

partition_key

partition_value

size_bytes

15. API interne

Publier data product :

POST /data-products

Lister versions :

GET /data-products/{id}/versions

Demander export :

POST /data-products/{id}/exports

16. Décisions d'architecture (ADR)

ADR-I13-001
Les bases transactionnelles ne servent pas de warehouse.

Décision :

Séparer charge applicative et charge analytique.

ADR-I13-002
Les datasets sont des produits.

Décision :

Chaque dataset a owner, SLA et contrat.

ADR-I13-003
Le stockage analytique supporte schema evolution.

Décision :

Permettre évolution sans migrations destructrices.

ADR-I13-004
Le coût data est attribuable.

Décision :

Piloter la croissance de stockage et compute.

17. Critères d'acceptation

Lakehouse conforme lorsque :

les zones raw/curated/serving existent ;
les data products sont catalogués ;
les schémas sont versionnés ;
les coûts sont mesurés ;
la rétention est appliquée ;
les exports sont gouvernés.

Décision majeure : Data Products First

La plateforme adopte une approche Data Products First.

La donnée n'est pas un sous-produit du code.

Elle devient une capacité exploitable et gouvernée.
