# Volume D03 — Engine Implementation Blueprint

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE D — ENGINEERING STANDARDS & IMPLEMENTATION BLUEPRINT
Volume D3
Engine Implementation Blueprint

Version : 1.0

Statut : Référence d'implémentation

Criticité : Critique

1. Vision

Un Engine est une unité fonctionnelle autonome.

Il possède :

son domaine métier ;
ses cas d'usage ;
ses événements ;
ses interfaces ;
ses adaptateurs ;
ses tests.

Un Engine n'accède jamais directement aux détails d'un autre Engine.

Il communique uniquement via :

Commands
Events
Internal Platform API
2. Blueprint universel

Tous les Engines respectent exactement cette structure.

engine/

├── bootstrap/
│
├── domain/
│
├── application/
│
├── ports/
│
├── adapters/
│
├── infrastructure/
│
├── contracts/
│
├── config/
│
├── migrations/
│
├── tests/
│
└── README.md
3. Domaine

Le domaine contient uniquement la logique métier.

domain/

entities/

aggregates/

services/

policies/

events/

value_objects/

exceptions/

Aucune dépendance technique.

4. Application

Cette couche orchestre.

application/

commands/

queries/

handlers/

use_cases/

dto/

validators/

Elle coordonne le domaine.

5. Ports

Les Ports représentent les interfaces.

ports/

repositories/

providers/

publishers/

gateways/

services/

Ils sont définis en Python sous forme de Protocol ou d'interfaces abstraites.

6. Adaptateurs

Ils implémentent les ports.

adapters/

postgres/

redis/

llm/

rest/

event_bus/

storage/

voice/

Ils contiennent le code dépendant des technologies.

7. Infrastructure
infrastructure/

dependency_injection/

config/

logging/

telemetry/

startup/

Cette couche relie le moteur au Kernel.

8. Bootstrap

Chaque moteur expose un point d'entrée unique.

initialize()

start()

stop()

health()

metadata()

Le Kernel ne connaît que ces fonctions.

9. Aggregate

Chaque Engine possède un Aggregate principal.

Exemple.

Conversation Engine.

ConversationAggregate

CRM Engine.

CustomerAggregate

Evaluation Engine.

EvaluationAggregate
10. Cycle d'un Use Case

Tous les cas d'usage suivent la même séquence.

Command

↓

Validation

↓

Use Case

↓

Aggregate

↓

Domain Events

↓

Persistence

↓

Publication Event Bus

↓

Response
11. Exemple

Commande.

StartSimulationCommand

↓

Handler.

StartSimulationHandler

↓

Use Case.

StartSimulationUseCase

↓

Aggregate.

SimulationAggregate

↓

Events.

SimulationStarted

↓

Projection.

12. DTO

Les DTO sont immuables.

Exemple.

SimulationDTO

ScenarioDTO

AgentDTO

SessionDTO

Ils ne contiennent aucune logique métier.

13. Validation

Les validations sont séparées.

Exemple.

Schema Validation

↓

Business Validation

↓

Rule Engine Validation

Chaque niveau a une responsabilité distincte.

14. Repositories

Les Repositories manipulent les agrégats.

Jamais les DTO.

Exemple.

ConversationRepository

SimulationRepository

ScenarioRepository
15. Providers

Les Providers représentent les services externes.

Exemple.

LLM Provider

Speech Provider

Storage Provider

Identity Provider

Notification Provider

Ils sont remplaçables.

16. Event Publisher

Tous les Engines utilisent la même interface.

publish(event)

publish_batch(events)

Le bus sous-jacent reste transparent.

17. Query Side

Les requêtes utilisent des Read Models.

Query

↓

Query Handler

↓

Read Model

↓

Response

Aucune logique métier.

18. Command Side

Les commandes modifient l'état.

Command

↓

Aggregate

↓

Events

Le CQRS est respecté.

19. Exemple : Conversation Engine
Conversation Engine

├── ConversationAggregate

├── StartConversationHandler

├── SendMessageHandler

├── ReceiveMessageHandler

├── ConversationRepository

├── LLMProvider

├── ConversationEvents

└── ConversationProjection
20. Exemple : CRM Engine
CRM Engine

├── CustomerAggregate

├── VerifyIdentityHandler

├── CreateTicketHandler

├── ApplyDiscountHandler

├── CustomerRepository

├── CRMEvents

└── CRMProjection
21. Exemple : Evaluation Engine
Evaluation Engine

├── EvaluationAggregate

├── ComputeScoreHandler

├── CoachingHandler

├── EvaluationRepository

├── RuleEvaluator

├── LLMEvaluator

└── EvaluationEvents
22. Health Check

Chaque moteur expose.

READY

RUNNING

FAILED

STOPPED

DEGRADED

Le Kernel centralise ces états.

23. Configuration

Chaque moteur possède son fichier.

engine.yaml

Exemple.

enabled: true

priority: 100

workers: 4

timeout: 10s

llm:
  enabled: true
24. Dépendances

Les dépendances sont déclarées.

Jamais implicites.

Exemple.

dependencies:

- event_bus

- kernel

- session_manager

- rule_engine

Le Boot Loader valide ces dépendances.

25. Tests

Chaque moteur doit disposer de.

Unit

Integration

Contract

Replay

Performance

Les tests de rejeu garantissent la compatibilité avec l'Event Sourcing.

26. Observabilité

Chaque moteur expose automatiquement.

Logs

Metrics

Traces

Health

Events

Aucun développement sans instrumentation.

27. Sécurité

Le contexte est propagé.

Tenant

Workspace

User

Role

Permissions

Trace ID

Aucune opération sans contexte.

28. Séquence complète
Client

↓

Gateway

↓

API

↓

Kernel

↓

Command

↓

Engine

↓

Aggregate

↓

Events

↓

Event Bus

↓

Projection

↓

Read Model

↓

API

↓

Client

Cette séquence est commune à tous les moteurs.

29. Matrice de responsabilités
Couche	Responsabilité	Dépend des couches
Domain	Règles métier	Aucune
Application	Cas d'usage	Domain
Ports	Contrats	Domain
Adapters	Intégrations techniques	Ports
Infrastructure	Wiring / DI	Ports + Adapters
Bootstrap	Cycle de vie	Infrastructure

Cette matrice constitue une règle d'architecture.

30. ADR

Ce volume fixe les décisions suivantes.

Tous les Engines suivent exactement le même Blueprint.
Les adaptateurs sont interchangeables.
Les agrégats sont la seule source de modification d'état.
Les DTO sont immuables.
Les Repositories manipulent les agrégats.
Les Providers encapsulent les services externes.
Les moteurs sont entièrement instrumentés.
31. Critères d'acceptation

Un Engine est considéré conforme lorsque :

il respecte la structure standard ;
il n'introduit aucune dépendance interdite ;
tous les cas d'usage passent par un Handler ;
les événements sont publiés via le EventPublisher ;
les tests couvrent le domaine, les contrats et les intégrations ;
le moteur peut être démarré et arrêté par le Kernel sans modification de celui-ci.
🏛️ Décision d'architecture majeure : Engine Development Kit (EDK)

Je recommande de créer un Engine Development Kit (EDK).

L'EDK est un générateur officiel de moteurs.

Une simple commande :

atos-cli engine create conversation

générerait automatiquement :

conversation/

├── bootstrap/
├── domain/
├── application/
├── ports/
├── adapters/
├── infrastructure/
├── contracts/
├── config/
├── tests/
├── README.md
└── engine.yaml

avec :

les interfaces de base ;
les tests unitaires initiaux ;
la configuration ;
les hooks d'observabilité ;
les fichiers ADR et README.

Cela garantit une homogénéité parfaite entre tous les Engines et accélère considérablement le développement.

📌 Évolution de la feuille de route

À ce stade, je recommande d'ajouter une Phase E, qui n'était pas prévue initialement mais qui apportera une valeur considérable :

Phase E — AI Engineering & Autonomous Development

Elle couvrira notamment :

E1 — Prompt Engineering Framework (prompts système, tâches, évaluateurs, garde-fous)
E2 — OpenCode Development Playbook (le prompt directeur complet pour OpenCode)
E3 — AI Coding Governance (règles de développement spécifiques aux agents IA)
E4 — RAG & Knowledge Base Architecture
E5 — LLMOps, évaluation des modèles et optimisation des coûts
E6 — AI QA & Validation Framework

Cette phase fera le lien entre toute l'architecture que nous avons définie et son implémentation par des agents IA, afin de disposer d'un véritable manuel de développement autonome pour conduire le projet jusqu'à la production. C'est cette phase qui fournira le prompt "maître" destiné à OpenCode.
