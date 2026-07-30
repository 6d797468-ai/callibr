# Volume J04 — Subscription, Entitlement & Plan Enforcement Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE J — ENTERPRISE PLATFORM SERVICES
Volume J04
Subscription, Entitlement & Plan Enforcement Architecture

Version : 1.0

Statut : Enterprise Commercial Runtime

Criticité : Critique

1. Vision

Le service d'entitlements traduit un contrat commercial en capacités produit exécutables.

Il répond :

ce tenant peut-il utiliser cette fonctionnalité ?
dans quelle limite ?
avec quel niveau de SLA ?
dans quel environnement ?

2. Principe fondamental

Le billing facture.

L'entitlement contrôle l'accès.

Les deux sont reliés mais séparés.

3. Architecture globale

                    Subscription


                         │


                         ▼


                  Entitlement Engine


        ┌────────────────┼────────────────┐


        ▼                ▼                ▼


 Feature Access      Quotas          Plan Limits

4. Entitlement Types

Types :

feature ;
quota ;
module ;
connector ;
domain pack ;
AI model ;
storage ;
support level ;
SLA ;
region.

5. Enforcement Points

Contrôle dans :

API Gateway ;
frontend ;
workers ;
AI Gateway ;
marketplace ;
connector runtime ;
reporting ;
exports.

6. Quotas

Exemples :

monthly_simulations ;
ai_tokens ;
voice_minutes ;
active_users ;
storage_gb ;
api_calls ;
domain_packs_installed ;
connectors_enabled.

7. Grace Period

Si dépassement :

warning ;
soft limit ;
hard limit ;
upgrade suggestion ;
admin notification ;
billing event.

8. Data Model

SubscriptionPlan
----------------

id

name

features

limits

Entitlement
-----------

id

tenant_id

key

value

source

status

UsageCounter
------------

id

tenant_id

metric

period

value

9. API interne

Vérifier entitlement :

POST /entitlements/check

Incrémenter usage :

POST /entitlements/usage

Lister droits tenant :

GET /entitlements/tenants/{tenant_id}

10. Décisions d'architecture (ADR)

ADR-J04-001
Les entitlements sont séparés du billing.

Décision :

Découpler finance et runtime produit.

ADR-J04-002
Les quotas sont appliqués par points d'exécution.

Décision :

Empêcher les contournements.

ADR-J04-003
Les dépassements produisent des événements.

Décision :

Relier usage, croissance et billing.

ADR-J04-004
Les plans sont versionnés.

Décision :

Préserver les contrats existants.

11. Critères d'acceptation

Entitlement Platform conforme lorsque :

les droits sont vérifiables par API ;
les quotas sont mesurés ;
les dépassements sont traités ;
les plans sont versionnés ;
les fonctionnalités sont bloquées si non autorisées ;
les événements alimentent billing et growth.

Décision majeure : Commercial Runtime Enforcement

Le contrat commercial devient exécutable par la plateforme.
