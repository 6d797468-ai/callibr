# Volume C01 — AI Training Operating System (ATOS) Kernel

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE C — PLATFORM CORE ARCHITECTURE
Volume C1
AI Training Operating System (ATOS) Kernel

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

La plupart des plateformes SaaS sont construites autour de modules.

Notre plateforme sera construite autour d'un Kernel.

Autrement dit :

Le Kernel ne connaît aucun métier.

Il fournit uniquement les services fondamentaux.

Les moteurs (Simulation, CRM, QA, Analytics…) deviennent des extensions.

Nous adoptons une architecture de type Micro-Kernel (Plug-in Architecture).

2. Pourquoi un Kernel ?

Aujourd'hui nous ciblons les centres de contacts.

Demain nous pourrons ajouter :

Banque
Assurance
Santé
Administration
Retail
Industrie
Aviation
Éducation
Défense
Logistique

Sans modifier le noyau.

3. Architecture globale
                   AI Training Operating System

                         ┌─────────────┐
                         │    Kernel   │
                         └──────┬──────┘
                                │
      ┌─────────────────────────┼──────────────────────────┐
      ▼                         ▼                          ▼
 Simulation Engine        CRM Runtime              Rule Engine
      ▼                         ▼                          ▼
 Conversation           Evaluation Engine         Analytics Engine
      ▼
 Prompt Engine

Le Kernel ne connaît pas les moteurs.

Il connaît uniquement leurs interfaces.

4. Services du Kernel

Le Kernel fournit :

Kernel

├── Configuration Service

├── Module Registry

├── Dependency Resolver

├── Event Bus

├── Session Manager

├── Lifecycle Manager

├── Security Context

├── Tenant Context

├── Scheduler

├── Health Manager

├── Metrics

├── Logging

├── Audit

└── Plugin Loader
5. Principes d'architecture

Le Kernel applique les principes suivants :

inversion des dépendances ;
injection de dépendances ;
modules découplés ;
interfaces stables ;
contrats versionnés ;
communication événementielle ;
configuration déclarative.
6. Couche Core

Le Core ne contient que :

core/

config/

kernel/

contracts/

events/

exceptions/

security/

telemetry/

Aucun code métier.

7. Couche Engines

Les moteurs vivent dans :

engines/

simulation/

conversation/

crm/

evaluation/

analytics/

prompt/

persona/

rule/

Chaque moteur est autonome.

8. Couche Domain Packs

Les métiers deviennent des packs.

domains/

telecom/

banking/

insurance/

energy/

health/

government/

retail/

Un Domain Pack contient :

scénarios ;
procédures ;
personas ;
règles ;
jeux de données ;
templates QA.
9. Couche Connectors

Les connecteurs sont indépendants.

connectors/

salesforce/

zendesk/

genesys/

twilio/

microsoft/

sap/

servicenow/

Le Kernel ignore leur implémentation.

10. Cycle de vie

Chaque moteur suit exactement le même cycle.

Discover

↓

Load

↓

Initialize

↓

Ready

↓

Running

↓

Pause

↓

Resume

↓

Stop

↓

Unload

Le Lifecycle Manager orchestre ces transitions.

11. Plugin Manifest

Chaque moteur fournit un manifeste déclaratif.

Exemple :

id: crm-runtime

name: CRM Runtime Engine

version: 1.0.0

api: 1.0

dependencies:
  - event-bus
  - session-manager
  - rule-engine

capabilities:
  - crm.commands
  - crm.events
  - crm.search

healthcheck:
  interval: 30s

permissions:
  - crm.read
  - crm.write
12. Contrats (Contracts)

Les moteurs communiquent via des interfaces.

Jamais via des classes concrètes.

Exemple :

ConversationEngine

↓

IConversationEngine
RuleEngine

↓

IRuleEngine

Le Kernel dépend uniquement des interfaces.

13. Registry

Tous les moteurs sont enregistrés.

Registry

↓

Simulation

↓

Conversation

↓

CRM

↓

QA

↓

Analytics

Le Registry est la source de vérité des composants disponibles.

14. Dependency Resolver

Le Kernel vérifie.

Exemple.

Conversation Engine

↓

Rule Engine requis

↓

Présent

↓

Chargement OK

Sinon.

Boot Failure
15. Capability Model

Un moteur annonce ses capacités.

Exemple.

crm.search

crm.commands

crm.events

crm.reporting

Le Kernel résout les dépendances par capacités, pas par implémentation.

16. Boot Process
Configuration

↓

Registry

↓

Plugins

↓

Dependencies

↓

Kernel Services

↓

Event Bus

↓

Engines

↓

Health Checks

↓

Ready

Chaque étape est journalisée.

17. Health Manager

Chaque moteur expose :

READY

RUNNING

DEGRADED

FAILED

STOPPED

Le Kernel surveille en continu leur état.

18. Configuration

Toute la configuration est déclarative.

tenant:

language:

llm_provider:

voice_enabled:

qa_enabled:

crm_enabled:

analytics_enabled:

Les paramètres sont validés au démarrage.

19. Extension

Pour ajouter un moteur :

Créer le plugin

↓

Déclarer le Manifest

↓

Implémenter les interfaces

↓

Déployer

↓

Boot

Aucune modification du Kernel n'est nécessaire.

20. Sécurité

Le Kernel fournit un contexte partagé.

Chaque requête transporte :

Tenant

↓

Workspace

↓

User

↓

Role

↓

Permissions

↓

Correlation ID

↓

Trace ID

Tous les moteurs utilisent ce contexte.

21. Observabilité

Chaque moteur publie :

métriques ;
logs structurés ;
traces distribuées ;
événements de santé.

Le Kernel agrège ces informations.

22. Versionnement

Le Kernel versionne :

API ;
contrats ;
événements ;
manifests ;
plugins.

Un plugin incompatible ne peut pas être chargé.

23. Décisions d'architecture (ADR)

Ce volume fixe les décisions suivantes :

Architecture micro-kernel.
Tous les moteurs sont des plugins.
Communication par contrats et événements.
Le Kernel ne contient aucune logique métier.
Les Domain Packs sont séparés des moteurs.
Les dépendances sont résolues au démarrage.
Les plugins sont versionnés indépendamment.
24. Structure cible du dépôt
atos/
│
├── kernel/
├── contracts/
├── events/
├── sdk/
├── engines/
│   ├── simulation/
│   ├── conversation/
│   ├── crm/
│   ├── rule/
│   ├── evaluation/
│   ├── analytics/
│   ├── persona/
│   └── prompt/
│
├── domains/
│   ├── telecom/
│   ├── banking/
│   ├── insurance/
│   ├── retail/
│   └── healthcare/
│
├── connectors/
├── api/
├── workers/
├── frontend/
├── tests/
├── docs/
└── deployment/

Cette structure sépare clairement le noyau, les moteurs, les packs métier et les connecteurs.

25. Critères d'acceptation

Le Kernel sera considéré conforme lorsque :

un nouveau moteur peut être ajouté sans modifier le code du Kernel ;
un Domain Pack peut être installé ou supprimé indépendamment ;
le cycle de vie des plugins est entièrement piloté par le Kernel ;
les interfaces publiques sont versionnées et stables ;
les moteurs communiquent exclusivement via les contrats et le bus d'événements ;
le système peut démarrer avec un sous-ensemble de moteurs (mode dégradé contrôlé).
🏛️ Décision d'architecture majeure (Architecture V3)

À ce stade, je recommande une évolution importante par rapport à une simple architecture micro-kernel : adopter une architecture hexagonale (Ports & Adapters) à l'intérieur de chaque moteur.

Cela signifie :

Le Kernel reste le point d'orchestration.
Chaque Engine devient une mini-application indépendante avec sa propre architecture hexagonale.
Les dépendances externes (LLM, PostgreSQL, Redis, Kafka, WebSocket, fournisseurs vocaux, etc.) sont implémentées comme des adaptateurs, jamais directement dans la logique métier.

Chaque moteur suivra une structure similaire :

engine/
├── domain/          # Entités, règles métier
├── application/     # Cas d'usage
├── ports/           # Interfaces
├── adapters/        # PostgreSQL, Redis, LLM, API...
├── infrastructure/  # Configuration technique
└── tests/

Cette combinaison Micro-Kernel + Event Sourcing + CQRS + Architecture Hexagonale est éprouvée pour des plateformes SaaS complexes et offre un excellent équilibre entre modularité, testabilité et évolutivité.

Prochaine étape

Le Volume C2 définira l'un des piliers techniques du système :

Event Bus, Event Sourcing & CQRS

Nous y spécifierons :

le schéma standard des événements ;
le bus d'événements interne ;
l'Event Store ;
les commandes (Commands) ;
les projections (Read Models) ;
le rejeu des simulations ;
l'idempotence ;
les garanties de livraison ;
les contrats d'événements versionnés.

Ce volume constituera la fondation de toute la communication entre les moteurs du système.
