# Volume I05 — Enterprise Integration Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE I — ENTERPRISE PRODUCT & BUSINESS PLATFORM
Volume I05
Enterprise Integration Platform Architecture

Version : 1.0

Statut : Enterprise Integration Foundation

Criticité : Critique

0. Note de nomenclature

Dans ce livre :

Callibr désigne le produit commercial et l'expérience SaaS.

ATOS désigne l'Operating System IA interne, c'est-à-dire le noyau technologique d'entraînement, de simulation, d'orchestration et d'évaluation.

Les intégrations Enterprise relient ces deux dimensions à l'écosystème réel du client.

1. Vision

Une plateforme SaaS Enterprise ne vit jamais seule.

Elle doit s'intégrer avec :

CRM ;
CCaaS ;
LMS ;
HRIS ;
ERP ;
BI ;
Identity Provider ;
Data Warehouse ;
outils qualité ;
outils de ticketing.

Objectif :

Transformer Callibr en plateforme connectée, gouvernée et observable.

2. Principe fondamental

Une intégration n'est jamais un script ponctuel.

C'est un produit technique durable.

Mauvais modèle :

Script

↓

Synchronisation

↓

Erreur silencieuse

Modèle Enterprise :

Connector

↓

Contract

↓

Mapping

↓

Sync Engine

↓

Observability

↓

Governance

3. Architecture globale

                    Enterprise Systems


                           │


                           ▼


                  Integration Platform


                           │


      ┌────────────────────┼────────────────────┐


      ▼                    ▼                    ▼


 Connector Runtime     Event Bridge         Sync Engine


      │                    │                    │


      ▼                    ▼                    ▼


 Canonical Model      Webhooks/API       Data Pipelines


                           │


                           ▼


                     Callibr / ATOS Core

4. Responsabilités

L'Enterprise Integration Platform fournit :

catalogue de connecteurs ;
authentification externe ;
gestion des secrets ;
mappage des données ;
synchronisation ;
webhooks ;
import/export ;
gestion des erreurs ;
observabilité ;
audit ;
rejeu ;
gouvernance.

5. Connector Runtime

Chaque connecteur est exécuté dans un runtime contrôlé.

Le runtime fournit :

configuration ;
authentification ;
quotas ;
retry ;
timeouts ;
circuit breaker ;
logs structurés ;
trace_id ;
tenant_id.

Un connecteur ne dialogue jamais directement avec le domaine.

Il passe par des ports d'intégration.

6. Types de connecteurs

Familles supportées :

CRM

Salesforce
HubSpot
Dynamics
Zendesk

CCaaS

Genesys
Talkdesk
Five9
Twilio
Amazon Connect

LMS

Moodle
Cornerstone
Docebo
360Learning

ITSM

ServiceNow
Jira Service Management
Freshservice

BI

Power BI
Tableau
Looker

Identity

Azure AD
Okta
Keycloak
Google Workspace

7. Connector Contract

Chaque connecteur expose un contrat standard.

Exemple :

connector:
  id: salesforce
  category: crm
  version: 1.0.0
  capabilities:
    - import_customers
    - export_results
    - sync_cases
    - receive_webhooks
  auth:
    type: oauth2
  limits:
    requests_per_minute: 500

Le contrat est versionné.

8. Canonical Data Model

Les systèmes externes possèdent des modèles différents.

Callibr adopte un modèle canonique.

Exemple :

External Contact

↓

Canonical Customer

↓

Simulation CRM Customer

Cette couche évite de contaminer le domaine avec des formats propriétaires.

9. Object Mapping

Mappages principaux :

ExternalUser

↓

CallibrUser

ExternalCustomer

↓

SimulatedCustomer

ExternalCase

↓

TrainingScenarioInput

ExternalTicket

↓

CRMCase

ExternalCourse

↓

TrainingProgram

10. Synchronisation

Trois modes sont supportés.

Batch Sync

Import planifié.

Near Real Time Sync

Synchronisation par événements.

On Demand Sync

Synchronisation déclenchée par l'utilisateur ou un workflow.

11. Sync Pipeline

Flux standard :

Source System

↓

Connector

↓

Extraction

↓

Validation

↓

Mapping

↓

Deduplication

↓

Persistence

↓

Event Publication

12. Event Bridge

L'Event Bridge relie les événements internes et externes.

Exemple :

SimulationCompleted

↓

Webhook

↓

LMS Result Updated

Autre exemple :

CRM Case Created

↓

Event Bridge

↓

Scenario Generated

13. Webhooks entrants

Les webhooks entrants sont contrôlés.

Vérifications :

signature ;
timestamp ;
replay protection ;
schema ;
tenant resolution ;
rate limit.

Aucun webhook ne modifie directement le domaine.

Il produit une commande ou un événement validé.

14. Webhooks sortants

Les webhooks sortants sont fiables.

Garanties :

signature HMAC ;
retry exponentiel ;
DLQ ;
historique ;
rejeu manuel ;
idempotency key ;
statut de livraison.

15. Identity Federation

Les intégrations Enterprise reposent souvent sur l'identité existante.

Support :

OIDC ;
SAML 2.0 ;
SCIM ;
Just-in-Time Provisioning ;
group mapping.

Objectif :

Créer les utilisateurs sans friction et conserver la gouvernance client.

16. SCIM Provisioning

Cycle :

Identity Provider

↓

SCIM

↓

Callibr Tenant

↓

Users / Groups / Roles

Les rôles sont mappés avec RBAC/ABAC.

17. Secret Management

Chaque intégration utilise des secrets.

Règles :

jamais en clair ;
chiffrement au repos ;
rotation ;
scoping par tenant ;
audit des accès ;
révocation immédiate.

18. Idempotence

Toute opération d'intégration doit être idempotente.

Exemple :

External Event

id: evt_123

Si l'événement est reçu deux fois :

une seule action métier est produite.

19. Rate Limiting externe

Chaque système externe possède ses limites.

Le Connector Runtime applique :

throttling ;
queueing ;
backoff ;
priorisation ;
fenêtres horaires.

L'objectif est de respecter les plateformes clientes.

20. Gestion des erreurs

Catégories :

erreur authentification ;
erreur quota ;
erreur schema ;
erreur mapping ;
erreur réseau ;
erreur métier ;
erreur permission.

Chaque erreur produit :

code ;
message ;
tenant ;
connector ;
trace_id ;
action recommandée.

21. Data Quality

Les données importées sont contrôlées.

Contrôles :

champs obligatoires ;
formats ;
unicité ;
références ;
valeurs interdites ;
données sensibles.

Les lignes rejetées sont historisées.

22. Integration Observability

Tableau de bord :

connecteurs actifs ;
latence ;
taux d'erreur ;
volumes synchronisés ;
événements en retard ;
retries ;
DLQ ;
coût API externe.

Chaque intégration est traçable de bout en bout.

23. Sandbox Integration

Les clients doivent tester avant production.

Environnements :

sandbox ;
staging ;
production.

Le connecteur peut être validé avec des jeux de données simulés.

24. Data Governance

Les intégrations respectent :

minimisation des données ;
classification ;
masquage ;
rétention ;
résidence ;
consentement ;
audit.

Les données externes ne sont importées que si elles servent un cas d'usage clair.

25. Data Model

Integration
-----------

id

tenant_id

connector_id

status

environment

created_at

ConnectorConfig
---------------

id

integration_id

auth_type

settings

secret_ref

SyncJob
-------

id

integration_id

mode

status

started_at

finished_at

IntegrationEvent
----------------

id

integration_id

event_type

external_id

idempotency_key

trace_id

26. API interne

Créer une intégration :

POST /integrations

Tester une connexion :

POST /integrations/{id}/test

Lancer une synchronisation :

POST /integrations/{id}/sync

Consulter les erreurs :

GET /integrations/{id}/errors

Rejouer un événement :

POST /integrations/events/{event_id}/replay

27. Décisions d'architecture (ADR)

ADR-I05-001
Les intégrations sont des produits techniques versionnés.

Décision :

Interdire les scripts non gouvernés pour les flux Enterprise.

ADR-I05-002
Le modèle canonique protège le domaine.

Décision :

Les formats propriétaires restent dans la couche connecteur.

ADR-I05-003
Toutes les synchronisations sont observables.

Décision :

Aucune intégration opaque n'est acceptée.

ADR-I05-004
Les webhooks sont signés, rejouables et idempotents.

Décision :

Garantir la fiabilité des échanges inter-systèmes.

28. Critères d'acceptation

Enterprise Integration Platform conforme lorsque :

✅ les connecteurs utilisent un runtime commun ;

✅ les contrats sont versionnés ;

✅ les secrets sont protégés ;

✅ les données sont mappées via un modèle canonique ;

✅ les synchronisations sont idempotentes ;

✅ les erreurs sont exploitables ;

✅ les flux sont observables ;

✅ les webhooks sont sécurisés et rejouables.

🏛️ Décision d'architecture majeure : Integration Control Plane (ICP)

La plateforme adopte un :

Integration Control Plane

qui relie :

Connector Runtime

+

Canonical Model

+

Sync Engine

+

Event Bridge

+

Security

+

Observability

Objectif :

Faire des intégrations une capacité Enterprise industrialisée, pas une collection de scripts fragiles.

📘 État d'avancement
Phase I — Enterprise Product & Business Platform

Terminé :

✅ I01 — Product Operating Model Architecture
✅ I02 — SaaS Multi-Tenant Architecture
✅ I03 — Customer Lifecycle Architecture
✅ I04 — Billing & Subscription Platform Architecture
✅ I05 — Enterprise Integration Platform Architecture

Restants :

I06 — API Ecosystem Architecture
I07 — Marketplace Architecture
I08 — Partner Platform Architecture
I09 — Revenue Architecture
I10 — Growth Engine Architecture

Prochaine étape :

Volume I06 — API Ecosystem Architecture

Ce volume définira la stratégie API publique, le portail développeur, les SDK, la compatibilité, les contrats, la gouvernance et la monétisation de l'écosystème API.
