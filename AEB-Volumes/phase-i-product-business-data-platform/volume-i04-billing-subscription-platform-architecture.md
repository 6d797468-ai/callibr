# Volume I04 — Billing & Subscription Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — ENTERPRISE PRODUCT & BUSINESS PLATFORM
Volume I04
Billing & Subscription Platform Architecture

Version : 1.0

Statut : Enterprise Revenue Foundation

Criticité : Critique

1. Vision

La Billing & Subscription Platform est le système financier du SaaS.

Elle relie :

                    Product Usage


                         │


                         ▼


                  Billing Platform


                         │


        ┌────────────────┼────────────────┐


        ▼                ▼                ▼


   Subscription      Metering        Payments


        │                │                │


        ▼                ▼                ▼


     Plans            Usage            Revenue

2. Principe fondamental

Un abonnement SaaS n'est pas seulement un paiement.

C'est un contrat entre :

une capacité produit ;
une consommation ;
un niveau de service ;
une valeur business.

Modèle simple :


Customer

↓

Plan

↓

Subscription

↓

Usage

↓

Invoice

↓

Payment
3. Billing Domain Architecture

Les domaines principaux :


Billing Platform


├── Product Catalog

├── Pricing Engine

├── Subscription Management

├── Usage Metering

├── Invoice Engine

├── Payment Processing

├── Tax Management

└── Revenue Analytics
4. Product Catalog

Le catalogue définit ce qui peut être vendu.

Exemples :

plans ;
modules ;
fonctionnalités ;
extensions.

Exemple :


product:

name:

AI Enterprise Platform


modules:

- AI Assistant

- Automation

- Analytics

- API Access

5. Pricing Model Architecture

Une plateforme SaaS peut utiliser plusieurs modèles.

Flat Rate

Prix fixe.

Exemple :

Plan Business

500 €/mois
Per User

Prix selon utilisateurs.

Exemple :

50 utilisateurs

× 20 €

=

1000 €/mois
Usage Based

Prix selon consommation.

Exemple :

Nombre workflows IA exécutés

×

prix unitaire
Hybrid Pricing

Combinaison :

Base abonnement

+

Consommation

+

Options
6. Subscription Lifecycle

Une souscription possède un cycle.


Created

↓

Active

↓

Upgrade

↓

Downgrade

↓

Suspended

↓

Cancelled

↓

Expired

7. Subscription Management

Une subscription contient :

client ;
plan ;
période ;
statut ;
limites ;
renouvellement.

Exemple :


{
"tenant":

"company_a",


"plan":

"enterprise",


"status":

"active",


"renewal":

"monthly"
}
8. Entitlement Management

Une partie essentielle SaaS :

Qu'est-ce que le client a le droit d'utiliser ?

Exemple :

Plan Starter :

5 utilisateurs

10 workflows IA

1 intégration

Plan Enterprise :

Utilisateurs illimités

Agents personnalisés

API complète

SLA

Architecture :


Subscription

↓

Entitlement Engine

↓

Feature Access

↓

Product Runtime
9. Feature Flag Billing Integration

Les fonctionnalités dépendent du plan.

Exemple :


feature:

advanced_agents


required_plan:

enterprise

Lors d'une demande :

User

↓

Feature Check

↓

Allowed ?

↓

Execute
10. Usage Metering Architecture

La consommation doit être mesurée.

Exemples :

appels IA ;
tokens ;
stockage ;
utilisateurs actifs ;
API calls ;
workflows.

Architecture :


Product Events

↓

Usage Collector

↓

Metering Engine

↓

Billing System

11. Usage Event Model

Chaque consommation devient un événement.

Exemple :


{
"type":

"ai_workflow_execution",


"tenant_id":

"tenant_001",


"quantity":

1,


"timestamp":

"2026-07-27"
}
12. AI Usage Billing

Pour une plateforme IA :

Mesures possibles :

tokens entrée ;
tokens sortie ;
temps GPU ;
appels modèle ;
stockage mémoire ;
exécutions agent.

Exemple :


Agent Support

↓

50000 requêtes

↓

Calcul coût

↓

Facturation
13. Invoice Engine

Le moteur de facture transforme l'utilisation en document financier.

Flux :


Usage

↓

Pricing Rules

↓

Invoice Generation

↓

Validation

↓

Delivery
14. Invoice Model

Une facture contient :

client ;
période ;
lignes ;
taxes ;
total ;
statut.

Exemple :


{
"customer":

"company_a",


"period":

"July 2026",


"amount":

"1250 €"
}
15. Payment Processing

Le paiement est séparé de la logique métier.

Architecture :


Billing Engine

↓

Payment Gateway

↓

Transaction

↓

Confirmation
16. Payment States

Cycle :


Pending

↓

Authorized

↓

Paid

↓

Failed

↓

Refunded
17. Payment Provider Abstraction

La plateforme ne dépend pas d'un seul fournisseur.

Architecture :


Billing Core

↓

Payment Adapter

↓

Provider A

Provider B

Provider C

Avantage :

changement fournisseur ;
multi-pays ;
résilience.
18. Credit Management

Les crédits permettent :

essais gratuits ;
compensation ;
promotions.

Exemple :


tenant:

company_a


credits:

5000


purpose:

trial_usage
19. Trial Management

Un essai possède :

durée ;
limites ;
conversion.

Flux :


Signup

↓

Trial Activated

↓

Usage

↓

Conversion

↓

Paid Subscription
20. Dunning Management

Gestion des paiements échoués.

Processus :


Payment Failed

↓

Retry

↓

Notification

↓

Grace Period

↓

Restriction
21. Revenue Recognition

Le revenu doit être suivi correctement.

Mesures :

MRR ;
ARR ;
expansion revenue ;
churn revenue.

Exemple :


MRR

=

revenu mensuel récurrent


ARR

=

MRR × 12

22. Billing Analytics

Dashboard :

Revenue
revenu mensuel ;
croissance ;
prévisions.
Usage
consommation ;
dépassements.
Customers
plans ;
upgrades ;
churn.
23. Data Model
Plan

Plan
----

id

name

price

billing_period

features
Subscription

Subscription
------------

id

tenant_id

plan_id

status

start_date

end_date
Usage Record

UsageRecord
-----------

id

tenant_id

metric

quantity

timestamp
Invoice

Invoice
-------

id

tenant_id

amount

status

due_date
24. API interne

Créer abonnement :

POST /billing/subscriptions

Obtenir consommation :

GET /billing/usage/{tenant_id}

Générer facture :

POST /billing/invoices/generate
25. Décisions d'architecture (ADR)
ADR-I04-001
Le billing est découplé du produit.

Décision :

La logique financière ne doit pas être dispersée dans les fonctionnalités.

ADR-I04-002
Toute consommation doit être mesurable.

Décision :

Impossible de facturer une ressource non observée.

ADR-I04-003
Les droits produit dépendent des entitlements.

Décision :

L'abonnement contrôle les capacités disponibles.

ADR-I04-004
Les fournisseurs de paiement sont abstraits.

Décision :

Éviter la dépendance technique unique.

26. Critères d'acceptation

Billing & Subscription Platform conforme lorsque :

✅ les plans existent ;

✅ les abonnements sont gérés ;

✅ les usages sont mesurés ;

✅ les fonctionnalités sont contrôlées ;

✅ les factures sont générées ;

✅ les paiements sont suivis ;

✅ les revenus sont analysables.

🏛️ Décision d'architecture majeure : Revenue Control Plane (RCP)

La plateforme adopte un :

Revenue Control Plane

qui relie :

Product

+

Usage

+

Subscription

+

Billing

+

Payment

+

Analytics

Objectif :

Créer un moteur économique SaaS prévisible.

📘 État d'avancement
Phase I — Enterprise Product & Business Platform

Terminé :

✅ I01 — Product Operating Model Architecture
✅ I02 — SaaS Multi-Tenant Architecture
✅ I03 — Customer Lifecycle Architecture
✅ I04 — Billing & Subscription Platform Architecture

Restants :

I05 — Enterprise Integration Platform
I06 — API Ecosystem Architecture
I07 — Marketplace Architecture
I08 — Partner Platform Architecture
I09 — Revenue Architecture
I10 — Growth Engine Architecture

Prochaine étape :

Volume I05 — Enterprise Integration Platform Architecture

Ce volume couvrira la connexion de la plateforme avec l'écosystème entreprise :

CRM ;
ERP ;
outils métiers ;
connecteurs ;
synchronisation données ;
webhooks ;
event bus ;
intégrations partenaires ;
architecture iPaaS.
