# Volume J10 — API Management, Developer Portal & Gateway Governance Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J10
API Management, Developer Portal & Gateway Governance Architecture

Version : 1.0

Statut : Enterprise API Operations

Criticité : Critique

1. Vision

L'API Management industrialise l'exposition des APIs Callibr.

Il couvre :

gateway ;
plans API ;
developer portal ;
credentials ;
quotas ;
analytics ;
changelog ;
deprecation ;
policies.

2. Principe fondamental

Une API publique est un produit opérable.

Elle doit être gouvernée comme une surface contractuelle Enterprise.

3. Architecture globale

                    API Consumers


                          │


                          ▼


                     API Gateway


       ┌──────────────────┼──────────────────┐


       ▼                  ▼                  ▼


 Policy Engine       Developer Portal      API Analytics

4. API Plans

Plans :

internal ;
partner ;
business ;
enterprise ;
strategic.

Chaque plan définit quotas, SLA et scopes disponibles.

5. Developer Portal

Fonctions :

docs ;
OpenAPI ;
SDK ;
sandbox ;
keys ;
webhook logs ;
status ;
support ;
usage.

6. Gateway Policies

Politiques :

auth ;
scope ;
tenant ;
schema validation ;
rate limit ;
payload size ;
IP allowlist ;
WAF ;
response filtering.

7. Deprecation Management

Cycle :

announcement ;
deprecated ;
migration window ;
sunset ;
removed.

8. Data Model

ApiProduct
----------

id

name

version

status

ApiPlan
-------

id

name

quotas

sla

ApiConsumer
-----------

id

tenant_id

application_id

plan_id

9. API interne

Créer API product :

POST /api-management/products

Associer plan :

POST /api-management/consumers/{id}/plan

Lire usage :

GET /api-management/usage

10. Décisions d'architecture (ADR)

ADR-J10-001
Les APIs sont packagées en produits.

Décision :

Relier usage, gouvernance et monétisation.

ADR-J10-002
Le Gateway applique les politiques.

Décision :

Centraliser contrôle et observabilité.

ADR-J10-003
Le portail développeur est obligatoire.

Décision :

Améliorer adoption et support.

ADR-J10-004
Les dépréciations sont gouvernées.

Décision :

Protéger les intégrations.

11. Critères d'acceptation

API Management conforme lorsque :

les API products existent ;
les plans contrôlent quotas ;
les credentials sont gérés ;
le portail expose docs et logs ;
les politiques gateway s'appliquent ;
les dépréciations sont traçables.

Décision majeure : Managed API Surface

La surface API devient une capacité Enterprise gouvernée.
