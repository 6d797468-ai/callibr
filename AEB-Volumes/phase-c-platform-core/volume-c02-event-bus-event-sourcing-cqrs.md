# Volume C02 — Event Bus, Event Sourcing & CQRS

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE C — PLATFORM CORE ARCHITECTURE
Volume C2
Event Bus, Event Sourcing & CQRS

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Toutes les actions effectuées dans la plateforme produisent des événements.

Exemple :

Agent envoie un message

↓

MessageSent
Ticket créé

↓

TicketCreated
Identité vérifiée

↓

IdentityVerified
Simulation terminée

↓

SimulationCompleted

L'état de la plateforme est reconstruit à partir de ces événements.

2. Pourquoi Event Sourcing ?

Au lieu de faire :

UPDATE session

SET status='finished'

nous faisons :

SimulationStarted

↓

GreetingDetected

↓

IdentityVerified

↓

TicketCreated

↓

SimulationCompleted

L'état final est calculé.

Il n'est jamais la source de vérité.

3. Architecture
                 Command

                    │

                    ▼

             Command Handler

                    │

                    ▼

             Rule Validation

                    │

                    ▼

               Domain Event

                    │

                    ▼

               Event Store

                    │

      ┌─────────────┼──────────────┐

      ▼             ▼              ▼

 Projection     Analytics     Read Models

      ▼

 REST API
4. Terminologie

Nous distinguons clairement :

Élément	Rôle
Command	Demande d'action
Event	Fait immuable
Aggregate	Cohérence métier
Projection	Vue de lecture
Read Model	Données optimisées pour la lecture
Snapshot	État périodique d'un Aggregate
5. Les Commands

Une Command représente une intention.

Exemple.

VerifyIdentityCommand
CreateTicketCommand
ApplyDiscountCommand

Une commande peut échouer.

6. Les Events

Un Event représente un fait.

Il ne change jamais.

Exemple.

IdentityVerified
TicketCreated
DiscountApplied

Les événements sont immuables.

7. Cycle
Utilisateur

↓

Command

↓

Validation

↓

Rule Engine

↓

Event

↓

Event Store

↓

Projection

↓

API

↓

Frontend
8. Structure standard d'un Event
event_id: UUID

event_type: TicketCreated

aggregate_type: Ticket

aggregate_id: TCK-001245

tenant_id: TENANT-001

workspace_id: TRAINING

session_id: SESSION-847

version: 3

occurred_at: 2026-08-01T10:15:23Z

causation_id: CMD-884

correlation_id: TRACE-001

actor:

  type: Agent

  id: AGENT-004

payload:

  priority: High

  category: Internet

metadata:

  schema_version: 1

  source: CRM Runtime
9. Event Store

L'Event Store contient uniquement des événements.

Jamais des états.

Event Store

↓

Event 1

↓

Event 2

↓

Event 3

↓

Event 4
10. Agrégats

Chaque Aggregate possède son flux.

Exemple.

Simulation

↓

SimulationCreated

↓

SimulationStarted

↓

ScenarioLoaded

↓

SimulationCompleted

Client.

Customer

↓

IdentityVerified

↓

AddressUpdated

↓

ContractChanged
11. Projections

Les projections construisent les vues.

Exemple.

Projection.

Session Dashboard

Construit à partir de.

Simulation Events

Projection.

CRM View

Construit à partir de.

Customer Events
12. Read Models

Les Read Models sont optimisés.

Exemple.

Agent Dashboard

↓

Lecture instantanée.

Aucune logique métier.

13. Snapshots

Pour éviter de rejouer 50 000 événements.

Le système crée périodiquement.

Snapshot

↓

Event 2500

Au redémarrage.

Snapshot

+

Events 2501...
14. Event Bus

Le bus diffuse.

TicketCreated

↓

Conversation Engine

↓

Analytics

↓

Evaluation

↓

Notifications

↓

Audit

Chaque moteur reçoit uniquement les événements auxquels il est abonné.

15. Topics

Le bus est organisé.

simulation.*

crm.*

conversation.*

qa.*

analytics.*

tenant.*

security.*

voice.*

system.*
16. Garanties

Le bus doit assurer.

ordre par Aggregate ;
livraison au moins une fois (at-least-once) ;
déduplication ;
reprise après incident ;
persistance.
17. Idempotence

Chaque consommateur doit être idempotent.

Exemple.

Deux événements.

TicketCreated

Ne créent jamais deux tickets.

18. Correlation ID

Toute la chaîne est traçable.

Simulation

↓

Command

↓

Event

↓

Projection

↓

Dashboard

Même Correlation ID.

19. Rejeu (Replay)

Le système peut rejouer.

Tous les événements

↓

Reconstruction

↓

Même état

Le rejeu sert à :

déboguer ;
recalculer des KPI ;
migrer des projections ;
entraîner de nouveaux modèles.
20. Versionnement

Les événements sont versionnés.

TicketCreated

v1

↓

v2

↓

v3

Les consommateurs doivent gérer plusieurs versions pendant les migrations.

21. Command Bus

Les commandes transitent également par un bus.

Frontend

↓

Command Bus

↓

Handler

↓

Rule Engine

↓

Aggregate

↓

Event

Cette séparation facilite les tests et l'extensibilité.

22. DLQ (Dead Letter Queue)

Les événements non traités sont isolés.

Erreur

↓

Retry

↓

Retry

↓

Retry

↓

DLQ

Aucun événement n'est perdu.

23. Observabilité

Chaque événement expose.

latence ;
temps de traitement ;
consommateur ;
statut ;
retries ;
erreurs.

Les métriques sont exportées vers Prometheus/OpenTelemetry.

24. Choix technologiques recommandés
Besoin	Recommandation
Event Bus	NATS JetStream (MVP) puis Apache Kafka (Enterprise)
Event Store	PostgreSQL (append-only) ou EventStoreDB
Serialization	JSON pour le MVP, Avro ou Protobuf pour Enterprise
Command Bus	Python (Mediator Pattern)
Projection Workers	Celery ou Dramatiq (MVP), Temporal ou Argo Workflows (Enterprise)
Traces	OpenTelemetry

Pourquoi NATS JetStream ?

Pour le MVP et les premières versions SaaS, NATS JetStream offre :

une faible latence ;
une administration simple ;
une excellente intégration avec Python ;
une montée en charge suffisante pour plusieurs milliers de simulations simultanées.

Kafka devient pertinent lorsque le volume d'événements et le nombre de consommateurs augmentent fortement.

25. Exemple complet
Agent

↓

VerifyIdentityCommand

↓

Rule Engine

↓

IdentityVerifiedEvent

↓

Event Store

↓

Projection CRM

↓

Projection Conversation

↓

Evaluation Engine

↓

Analytics Engine

↓

Dashboard mis à jour

Tout est piloté par le même événement.

26. Contrat d'un événement

Tous les événements implémentent une interface commune.

class DomainEvent(Protocol):
    event_id: UUID
    event_type: str
    aggregate_id: str
    aggregate_type: str
    occurred_at: datetime
    tenant_id: str
    version: int
    payload: dict

Les moteurs manipulent ce contrat, jamais une implémentation spécifique.

27. Décisions d'architecture (ADR)

Ce volume fixe plusieurs décisions majeures :

L'Event Store est la source de vérité.
Les bases relationnelles servent principalement aux projections et aux requêtes.
Toutes les actions métier passent par des Commands.
Tous les faits métier sont représentés par des Events immuables.
Les moteurs communiquent exclusivement via le bus d'événements.
Les événements sont versionnés et compatibles avec les évolutions de schéma.
28. Critères d'acceptation

L'architecture Event Sourcing + CQRS sera considérée conforme lorsque :

une simulation complète peut être reconstruite uniquement à partir des événements ;
les projections peuvent être supprimées puis régénérées ;
les événements sont immuables et versionnés ;
le rejeu produit un état identique ;
les consommateurs sont idempotents ;
les erreurs de traitement sont isolées sans perte d'événements.
🏛️ Décision d'architecture majeure : Internal Platform API (IPA)

À partir de ce volume, je recommande une évolution supplémentaire : aucun moteur ne doit appeler directement un autre moteur.

Les échanges se font exclusivement selon deux mécanismes :

Commandes synchrones (quand une réponse immédiate est nécessaire).
Événements asynchrones (pour notifier les changements d'état).

Cette règle garantit un découplage fort, facilite les tests, améliore la résilience et permet de remplacer ou de faire évoluer un moteur sans impact sur les autres.

Prochain volume : C3 — Multi-Tenant SaaS Architecture

Nous définirons :

l'isolation des tenants ;
les organisations et workspaces ;
les rôles (RBAC) et les attributs (ABAC) ;
les licences et quotas ;
la hiérarchie Entreprise → Business Unit → Campagne → Équipe → Agent ;
les stratégies de partitionnement des données ;
les modèles de déploiement (SaaS partagé, dédié et on-premise).

Ce volume transformera l'architecture en une véritable plateforme SaaS Enterprise prête pour une exploitation à grande échelle.
