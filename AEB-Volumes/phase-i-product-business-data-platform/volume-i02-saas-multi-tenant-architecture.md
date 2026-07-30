# Volume I02 — SaaS Multi-Tenant Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — ENTERPRISE PRODUCT & BUSINESS PLATFORM
Volume I02
SaaS Multi-Tenant Architecture

Version : 1.0

Statut : Enterprise SaaS Foundation

Criticité : Critique

1. Vision

Une architecture Multi-Tenant permet à une seule plateforme de servir plusieurs organisations clientes tout en maintenant :

isolation des données ;
isolation sécurité ;
personnalisation ;
gouvernance ;
performance.

Architecture :

                    SaaS Platform


                         │


        ┌────────────────┼────────────────┐


        ▼                ▼                ▼


     Tenant A         Tenant B         Tenant C


        │                │                │


        ▼                ▼                ▼


    Data A           Data B           Data C

2. Principe fondamental

Un client SaaS n'est jamais un simple utilisateur.

Il représente une organisation complète.

Modèle :

Tenant

│

├── Users

├── Roles

├── Data

├── Configuration

├── Billing

├── AI Policies

└── Integrations
3. Architecture Multi-Tenant

Trois grands modèles existent.

Modèle 1 — Shared Database / Shared Schema

Tous les tenants partagent les mêmes tables.

Exemple :

customers

----------------

id

tenant_id

name

email

Séparation :

tenant_id

Avantages :

✅ coût faible
✅ simple à scaler

Inconvénients :

⚠️ risque fuite données
⚠️ isolation plus complexe

Modèle 2 — Shared Database / Separate Schema

Une base commune avec schémas séparés.

Exemple :

Database

├── tenant_a_schema

├── tenant_b_schema

└── tenant_c_schema

Avantages :

✅ meilleure isolation
✅ gestion plus claire

Inconvénients :

⚠️ migrations plus complexes

Modèle 3 — Database per Tenant

Chaque client possède sa propre base.

Architecture :

Tenant A

↓

Database A


Tenant B

↓

Database B

Avantages :

✅ isolation maximale
✅ conformité facilitée

Inconvénients :

⚠️ coût infrastructure supérieur

4. Architecture recommandée Enterprise

Pour une plateforme IA SaaS Enterprise :

Approche hybride.

                    SaaS Core


                         │


          ┌──────────────┼──────────────┐


          ▼              ▼              ▼


      Small Tenants   Medium       Enterprise


      Shared DB       Schema       Dedicated DB


Pourquoi ?

Parce que tous les clients n'ont pas les mêmes exigences.

5. Tenant Identity Model

Chaque requête doit connaître son tenant.

Flux :

User Request

↓

Authentication

↓

Tenant Resolution

↓

Authorization

↓

Business Logic

↓

Data Access


Exemple Token :

{
"user_id":

"usr_100",


"tenant_id":

"company_abc",


"role":

"admin"
}
6. Tenant Isolation Layer

Couche obligatoire.

Architecture :

Application

↓

Tenant Context

↓

Policy Enforcement

↓

Database


Règle :

Aucune requête ne doit accéder aux données sans contexte tenant.

7. Tenant Context Propagation

Le tenant doit voyager dans tout le système.

Exemple :

API Gateway

tenant_id

↓

Backend Service

tenant_id

↓

AI Agent

tenant_id

↓

Database Query

tenant_id

8. Data Isolation

Toutes les données métier portent un tenant.

Exemple :

CREATE TABLE conversations
(
id UUID,

tenant_id UUID,

user_id UUID,

message TEXT
);
9. Row Level Security (RLS)

Protection supplémentaire côté base.

Exemple :

Policy:

ALLOW READ

WHERE

tenant_id = current_tenant

Même avec un bug applicatif :

La base bloque.

10. Tenant Configuration

Chaque entreprise possède sa configuration.

Exemple :

tenant:

name:

Company A


settings:

language:

fr


timezone:

Europe/Paris


ai_policy:

strict
11. Tenant Customization

Une plateforme Enterprise doit permettre :

branding ;
workflows ;
règles métier ;
agents personnalisés ;
intégrations.

Architecture :

Core Platform

+

Tenant Configuration

=

Customized Experience
12. User & Organization Model

Structure :

Organization

│

├── Workspace

│

├── Teams

│

├── Users

│

└── Roles

Exemple :

Entreprise ABC

 ├── Direction

 ├── Support

 └── Finance

13. Role Based Access Control (RBAC)

Les permissions dépendent du rôle.

Exemple :

role:

support_manager


permissions:

- view_customer

- assign_ticket

- export_report
14. Attribute Based Access Control (ABAC)

Pour les cas complexes.

Décision selon :

rôle ;
département ;
localisation ;
contexte ;
niveau risque.

Exemple :

User:

Finance Manager


Can access:

Invoices


Cannot access:

HR Data
15. Tenant AI Isolation

Dans une plateforme IA :

La séparation doit inclure :

conversations ;
mémoire ;
embeddings ;
datasets ;
agents.

Architecture :

Tenant A

↓

Vector Namespace A


Tenant B

↓

Vector Namespace B

16. Multi-Tenant Vector Database

Exemple :

Qdrant Collection


tenant_a_vectors


tenant_b_vectors


tenant_c_vectors

Recherche :

{
"filter":

{
"tenant_id":

"company_a"
}
}
17. Tenant Resource Quotas

Chaque tenant possède des limites.

Exemple :

tenant:

plan:

business


limits:

users:
100


ai_requests_month:
50000

Protection :

surcharge ;
abus ;
explosion coût.
18. Tenant Billing Isolation

Chaque consommation doit être attribuée.

Flux :

Tenant

↓

Usage Tracking

↓

Metering

↓

Billing

↓

Invoice
19. Tenant Lifecycle

Un tenant possède un cycle de vie.

Created

↓

Setup

↓

Active

↓

Suspended

↓

Archived

20. Tenant Provisioning

Création automatique :

New Customer

↓

Create Tenant

↓

Create Workspace

↓

Initialize Database

↓

Create Admin

↓

Activate
21. Tenant Migration

Un client peut évoluer.

Exemple :

Shared Database

↓

Dedicated Database

Migration :

export ;
transfert ;
validation ;
bascule.
22. Multi-Tenant Observability

Toutes les métriques doivent être filtrables.

Exemple :

{
"tenant":

"company_a",


"requests":

50000,


"errors":

12
}
23. Tenant Security Audit

Audit par client :

connexions ;
actions ;
accès données ;
changements configuration.
24. Data Model
Tenant
Tenant
------

id

name

plan

status

created_at
Workspace
Workspace
---------

id

tenant_id

name

settings
Membership
Membership
----------

id

tenant_id

user_id

role
Tenant Configuration
TenantConfig
------------

id

tenant_id

key

value
25. API interne

Créer un tenant :

POST /tenants

Payload :

{
"name":

"Company ABC",

"plan":

"enterprise"
}

Résultat :

{
"tenant_id":

"tenant_001",

"status":

"active"
}
26. Décisions d'architecture (ADR)
ADR-I02-001
Le tenant est une frontière de sécurité.

Décision :

Toutes les données doivent être isolées par tenant.

ADR-I02-002
L'identité tenant est propagée partout.

Décision :

Aucun service ne travaille sans contexte organisationnel.

ADR-I02-003
L'architecture supporte plusieurs niveaux d'isolation.

Décision :

Adapter l'isolation au niveau client.

ADR-I02-004
Les ressources sont gouvernées par tenant.

Décision :

Prévenir abus et surconsommation.

27. Critères d'acceptation

La SaaS Multi-Tenant Architecture est conforme lorsque :

✅ les tenants sont isolés ;

✅ les utilisateurs appartiennent à une organisation ;

✅ les permissions sont contrôlées ;

✅ les données IA sont séparées ;

✅ les quotas existent ;

✅ le provisioning est automatisable ;

✅ les audits sont possibles.

🏛️ Décision d'architecture majeure : Tenant Control Plane (TCP)

La plateforme adopte un :

Tenant Control Plane

qui orchestre :

Tenant

+

Identity

+

Security

+

Data

+

AI Context

+

Billing

pour fournir une base SaaS Enterprise solide.

📘 État d'avancement
Phase I — Enterprise Product & Business Platform

Terminé :

✅ I01 — Product Operating Model Architecture
✅ I02 — SaaS Multi-Tenant Architecture

Restants :

I03 — Customer Lifecycle Architecture
I04 — Billing & Subscription Platform
I05 — Enterprise Integration Platform
I06 — API Ecosystem Architecture
I07 — Marketplace Architecture
I08 — Partner Platform Architecture
I09 — Revenue Architecture
I10 — Growth Engine Architecture

Prochaine étape :

Volume I03 — Customer Lifecycle Architecture

Ce volume définira le parcours complet client Enterprise :

acquisition ;
onboarding ;
activation ;
adoption ;
expansion ;
renouvellement ;
churn prevention ;
customer success.
