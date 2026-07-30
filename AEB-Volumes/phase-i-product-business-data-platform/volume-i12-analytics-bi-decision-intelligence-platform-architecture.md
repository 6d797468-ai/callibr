# Volume I12 — Analytics, BI & Decision Intelligence Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I12
Analytics, BI & Decision Intelligence Platform Architecture

Version : 1.0

Statut : Enterprise Analytics Foundation

Criticité : Critique

1. Vision

La plateforme Analytics transforme les événements et données opérationnelles en décisions.

Elle sert :

agents ;
formateurs ;
superviseurs ;
WFM ;
QA ;
direction ;
Customer Success ;
finance ;
équipes produit.

2. Principe fondamental

Un tableau de bord n'est pas une architecture data.

L'architecture correcte sépare :

collecte ;
modélisation ;
qualité ;
métriques ;
visualisation ;
gouvernance.

3. Architecture globale

                    Event Store / Sources


                            │


                            ▼


                     Analytics Pipeline


                            │


            ┌───────────────┼───────────────┐


            ▼               ▼               ▼


       Metrics Store    Semantic Layer     BI Portal


            │               │               │


            ▼               ▼               ▼


       KPI Engine       Dashboards      Decision Support

4. Analytics Domains

Domaines :

training analytics ;
quality analytics ;
conversation analytics ;
CRM analytics ;
WFM analytics ;
AI cost analytics ;
tenant analytics ;
product analytics ;
revenue analytics ;
security analytics.

5. Metrics Layer

Chaque métrique doit avoir :

nom ;
définition ;
formule ;
owner ;
source ;
grain ;
période ;
filtre tenant ;
contrôle qualité.

6. Metric Contract

Exemple :

metric:
  id: simulation_success_rate
  owner: learning_analytics
  formula: successful_simulations / completed_simulations
  grain: tenant_day
  dimensions:
    - tenant_id
    - domain_pack
    - agent_level

7. KPI Engine

Le KPI Engine calcule :

valeurs ;
tendances ;
comparaisons ;
alertes ;
objectifs ;
écarts ;
benchmarks.

8. Semantic Layer

Le Semantic Layer donne un vocabulaire commun.

Exemple :

"session terminée"

doit signifier la même chose pour :

BI ;
produit ;
finance ;
learning ;
QA.

9. Dashboard Architecture

Types :

dashboard agent ;
dashboard formateur ;
dashboard superviseur ;
dashboard direction ;
dashboard tenant admin ;
dashboard AI Ops ;
dashboard revenue.

Chaque dashboard consomme des métriques gouvernées.

10. Decision Intelligence

La plateforme ne montre pas seulement des chiffres.

Elle propose :

diagnostics ;
causes probables ;
actions recommandées ;
priorités ;
impact attendu.

Les recommandations restent explicables.

11. Data Freshness

Niveaux :

temps réel ;
near real time ;
horaire ;
quotidien ;
mensuel.

Chaque métrique déclare sa fraîcheur attendue.

12. Multi-Tenant Analytics

Règles :

filtrage tenant obligatoire ;
agrégats anonymisés ;
benchmark opt-in ;
pas de fuite inter-client ;
permissions analytiques par rôle.

13. Benchmarking

Le benchmark compare :

équipes ;
campagnes ;
domain packs ;
sites ;
périodes ;
cohortes.

Les comparaisons inter-tenants exigent anonymisation et consentement.

14. Data Quality Checks

Contrôles :

complétude ;
unicité ;
fraîcheur ;
cohérence ;
plage de valeurs ;
drift ;
volumes inattendus.

15. BI Export

Sorties :

CSV ;
Parquet ;
API ;
Power BI ;
Tableau ;
Looker ;
Warehouse client.

Les exports respectent RBAC/ABAC.

16. Data Model

MetricDefinition
----------------

metric_id

name

formula

owner

grain

status

MetricValue
-----------

metric_id

tenant_id

dimensions

period_start

period_end

value

Dashboard
---------

id

tenant_id

name

audience

widgets

17. API interne

Lister métriques :

GET /analytics/metrics

Calculer KPI :

POST /analytics/kpi/calculate

Lire dashboard :

GET /analytics/dashboards/{id}

Exporter :

POST /analytics/exports

18. Décisions d'architecture (ADR)

ADR-I12-001
Les KPI sont définis comme des contrats.

Décision :

Éviter les définitions contradictoires.

ADR-I12-002
Le Semantic Layer est obligatoire.

Décision :

Créer une langue commune entre métiers et technique.

ADR-I12-003
Les benchmarks inter-tenants sont anonymisés.

Décision :

Protéger la confidentialité client.

ADR-I12-004
Les dashboards consomment des métriques gouvernées.

Décision :

Réduire les décisions basées sur des chiffres non validés.

19. Critères d'acceptation

Analytics Platform conforme lorsque :

les métriques ont une définition stable ;
les dashboards utilisent le Semantic Layer ;
les exports sont contrôlés ;
les KPI sont recalculables ;
les benchmarks sont sécurisés ;
les anomalies data sont détectées.

Décision majeure : Governed Metrics Platform

Callibr adopte une Governed Metrics Platform.

La donnée analytique devient un produit gouverné.
