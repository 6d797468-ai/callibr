# Volume I20 — Real-Time Data Streaming & Operational Intelligence Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — DATA PLATFORM & KNOWLEDGE SYSTEM
Volume I20
Real-Time Data Streaming & Operational Intelligence Architecture

Version : 1.0

Statut : Enterprise Real-Time Foundation

Criticité : Critique

1. Vision

Le Real-Time Data Streaming permet à Callibr de réagir aux événements pendant qu'ils se produisent.

Cas d'usage :

supervision temps réel ;
conversation live ;
alertes QA ;
coaching immédiat ;
WFM intraday ;
détection d'anomalies ;
AI Ops ;
sécurité ;
facturation usage.

2. Principe fondamental

Le temps réel n'est pas une version rapide du batch.

Il exige :

événements légers ;
faible latence ;
backpressure ;
ordre local ;
idempotence ;
fenêtrage ;
monitoring ;
dégradation contrôlée.

3. Architecture globale

                    Event Producers


                          │


                          ▼


                    Streaming Bus


       ┌──────────────────┼──────────────────┐


       ▼                  ▼                  ▼


 Stream Processing   Real-Time Views    Alert Engine


       │                  │                  │


       ▼                  ▼                  ▼


 Dashboards Live     Operational API     Automation

4. Streaming Topics

Topics :

conversation.turns ;
simulation.events ;
crm.actions ;
evaluation.signals ;
wfm.intraday ;
ai.runtime ;
security.events ;
billing.usage ;
integration.status.

5. Stream Processing

Traitements :

filter ;
aggregate ;
join ;
window ;
enrich ;
detect ;
route ;
alert.

6. Windowing

Fenêtres :

tumbling ;
sliding ;
session windows ;
event-time ;
processing-time.

Exemple :

taux d'abandon sur les 5 dernières minutes.

7. Backpressure

Le système doit gérer :

pics de trafic ;
consommateurs lents ;
LLM ralentis ;
exports lourds ;
défaillances réseau.

8. Real-Time Views

Vues :

queue status ;
live simulation status ;
agent activity ;
AI latency ;
cost burn rate ;
alert feed ;
security events.

9. Alert Engine

Une alerte possède :

condition ;
seuil ;
fenêtre ;
priorité ;
destinataire ;
action ;
escalade ;
silencing.

10. Operational Intelligence

Le système propose :

cause probable ;
impact ;
urgence ;
actions possibles ;
risques ;
historique similaire.

11. Delivery Guarantees

Garanties selon cas :

at-most-once pour télémétrie non critique ;
at-least-once pour events métier ;
exactly-once logique par idempotence.

12. Data Model

StreamTopic
-----------

id

name

schema_ref

retention

owner

StreamConsumer
--------------

id

topic_id

consumer_group

lag

status

AlertRule
---------

id

tenant_id

metric

condition

severity

action

13. API interne

Créer topic :

POST /streaming/topics

Consulter lag :

GET /streaming/consumers/{id}/lag

Créer alerte :

POST /streaming/alerts/rules

14. Décisions d'architecture (ADR)

ADR-I20-001
Le streaming est séparé du batch.

Décision :

Optimiser chaque mode selon ses contraintes.

ADR-I20-002
Les garanties sont choisies par cas d'usage.

Décision :

Éviter un coût technique excessif.

ADR-I20-003
Les vues temps réel sont dérivées d'événements.

Décision :

Conserver cohérence et rejouabilité partielle.

ADR-I20-004
Les alertes sont gouvernées.

Décision :

Réduire fatigue d'alerte et bruit opérationnel.

15. Critères d'acceptation

Streaming Platform conforme lorsque :

les topics sont catalogués ;
les schémas sont versionnés ;
le lag est mesuré ;
les alertes sont configurables ;
les vues temps réel sont isolées par tenant ;
la dégradation contrôlée est testée.

Décision majeure : Real-Time Operational Nervous System

Callibr adopte un système nerveux opérationnel temps réel.

Les événements deviennent actionnables pendant que la simulation, l'apprentissage et l'exploitation se déroulent.

Fin de l'extension Phase I — Data Platform & Knowledge System

La Data Platform couvre désormais :

I11 — Event Store, Data Contracts & Canonical Event Model
I12 — Analytics, BI & Decision Intelligence
I13 — Lakehouse, Warehouse & Data Products
I14 — Feature Store & ML Data Platform
I15 — Vector Database, Embeddings & Semantic Retrieval
I16 — Knowledge Graph & Semantic Layer
I17 — Data Governance, Privacy & Quality
I18 — Audit, Lineage & Compliance Data
I19 — KPI, Reporting & Executive Intelligence
I20 — Real-Time Data Streaming & Operational Intelligence

Prochaine phase recommandée :

Phase J — Enterprise Platform Services

Elle devra couvrir :

IAM ;
RBAC / ABAC ;
Organizations ;
Tenants ;
Subscriptions ;
Plugins ;
Extensions ;
White Label ;
Localization ;
Compliance ;
GDPR ;
API Management ;
Enterprise Integrations.

PHASE J — ENTERPRISE PLATFORM SERVICES

Objectif de la phase

La Phase J définit les services transverses nécessaires pour transformer Callibr en plateforme Enterprise exploitable à grande échelle.

Les phases précédentes ont défini les moteurs métier, IA, data et produit.

La Phase J définit maintenant les services partagés qui gouvernent :

identité ;
permissions ;
organisations ;
tenants ;
abonnements ;
entitlements ;
plugins ;
extensions ;
white label ;
localisation ;
conformité ;
API management ;
intégrations ;
notifications ;
administration.

Principe directeur

Un service Enterprise doit être :

multi-tenant ;
observable ;
auditable ;
configurable ;
sécurisé ;
testable ;
versionné ;
exploitable par API.
