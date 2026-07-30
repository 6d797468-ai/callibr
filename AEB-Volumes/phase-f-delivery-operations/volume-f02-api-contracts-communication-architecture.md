# Volume F02 — API Contracts & Communication Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE F — DELIVERY, IMPLEMENTATION & ENTERPRISE OPERATIONS
Volume F2
API Contracts & Communication Architecture

Version : 1.0

Statut : Référence d'implémentation

Criticité : Critique

1. Vision

Dans ATOS, aucun composant ne communique librement avec un autre.

Toute communication passe par un contrat explicite.

Les contrats constituent une API de plateforme.

Le code est libre de changer.

Les contrats sont stables.

2. Architecture de communication
                Client Web

                     │

              API Gateway

         ┌───────────┼───────────┐

         ▼           ▼           ▼

      REST API   WebSocket   Streaming

         ▼           ▼           ▼

              Platform Kernel

                     │

          Internal Command Bus

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

 Conversation    CRM Engine   Evaluation

        ▼            ▼            ▼

             Internal Event Bus

                     │

          Analytics / Read Models
3. Types de communication

ATOS distingue cinq familles.

Type	Usage
REST	CRUD et opérations synchrones
WebSocket	Temps réel
Event Bus	Communication interne
Command Bus	Exécution métier
Streaming	Audio / Voix

Chaque famille possède ses conventions.

4. REST API

REST est réservé aux opérations synchrones.

Exemples :

POST /api/v1/simulations

GET /api/v1/simulations/{id}

POST /api/v1/scenarios

GET /api/v1/personas

Les règles REST suivent OpenAPI 3.1.

5. Versionnement

Toutes les API publiques sont versionnées.

Exemple.

/api/v1/

/api/v2/

Aucune rupture de compatibilité dans une même version majeure.

6. Format de réponse

Toutes les réponses utilisent une enveloppe standard.

{
  "success": true,
  "data": {},
  "metadata": {},
  "errors": [],
  "trace_id": "..."
}

Cette structure est uniforme.

7. Gestion des erreurs

Format unique.

{
  "success": false,
  "error": {
    "code": "IDENTITY_NOT_VERIFIED",
    "message": "...",
    "details": {},
    "trace_id": "..."
  }
}

Les codes sont documentés.

8. Pagination

Convention unique.

page

page_size

total

has_next

Les curseurs sont utilisés pour les très gros volumes.

9. WebSocket

Utilisé pour :

conversation IA ;
notifications ;
streaming vocal ;
CRM temps réel ;
progression de simulation.
10. Messages WebSocket

Structure.

{
  "type": "conversation.message",
  "session_id": "...",
  "timestamp": "...",
  "payload": {}
}

Chaque message est typé.

11. Types d'événements WebSocket

Exemples.

session.started

session.ended

message.received

message.generated

crm.updated

emotion.changed

evaluation.updated

voice.partial

voice.final

Les noms suivent la convention domaine.action.

12. Command Bus

Les Commands modifient l'état.

Exemple.

StartSimulation

VerifyIdentity

OpenTicket

ApplyCompensation

EndConversation

Une Command possède un seul Handler.

13. Structure Command
{
  "command_id": "...",
  "tenant_id": "...",
  "session_id": "...",
  "type": "VerifyIdentity",
  "payload": {}
}
14. Query Bus

Les Queries lisent uniquement.

Exemples.

GetScenario

GetSimulation

GetEvaluation

GetCustomer

GetTimeline

Aucun effet de bord.

15. Event Bus

Les événements représentent des faits.

Exemple.

SimulationStarted

IdentityVerified

CustomerCalmedDown

TicketCreated

SimulationFinished

EvaluationCompleted

Les événements sont immuables.

16. Structure Event
{
  "event_id": "...",
  "aggregate_id": "...",
  "event_type": "...",
  "version": 1,
  "timestamp": "...",
  "payload": {}
}
17. Compatibilité

Les événements :

ne sont jamais modifiés ;
sont uniquement enrichis ;
restent compatibles avec les consommateurs existants.

Les changements incompatibles créent une nouvelle version.

18. Contrats CRM

Le CRM simulé expose des capacités.

Exemples.

VerifyIdentity

SearchCustomer

CreateTicket

ApplyCredit

CancelOrder

UpdateAddress

Le LLM ne modifie jamais directement le CRM.

Toutes les actions passent par des Commands.

19. Contrats Voice

Le moteur Voice expose.

StartRecognition

StopRecognition

SpeechChunk

TranscriptFinal

StartSynthesis

AudioGenerated

Les flux audio sont séparés des flux conversationnels.

20. API Gateway

Responsabilités.

authentification ;
autorisation ;
limitation de débit ;
journalisation ;
routage ;
versionnement.

La Gateway ne contient pas de logique métier.

21. Authentification

Support prévu.

OAuth2
OpenID Connect
JWT
API Keys (intégrations serveur à serveur)

Les identités sont propagées jusqu'aux Engines.

22. Contexte

Chaque requête transporte.

tenant_id:

workspace_id:

user_id:

session_id:

trace_id:

correlation_id:

Le contexte est obligatoire.

23. Idempotence

Les opérations critiques acceptent une clé d'idempotence.

Exemple.

Idempotency-Key

Cela évite les doublons lors des réessais.

24. Documentation

Toutes les API sont décrites par.

OpenAPI 3.1
AsyncAPI (WebSocket/Event Bus)
JSON Schema

Les SDK sont générés à partir de ces contrats.

25. Tests de contrat

Chaque contrat possède.

tests REST ;
tests WebSocket ;
tests d'événements ;
tests de compatibilité.

Les consommateurs et producteurs sont validés automatiquement.

26. Observabilité

Toutes les communications génèrent.

logs ;
métriques ;
traces distribuées ;
événements d'audit.

Chaque appel est corrélable via le trace_id.

27. Sécurité

Les contrats imposent.

validation des schémas ;
contrôle RBAC/ABAC ;
limitation de débit ;
protection contre la rejeu des requêtes ;
chiffrement TLS.
28. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les contrats sont la seule interface entre les composants.
Les API publiques sont versionnées.
Les événements sont immuables.
Les Commands modifient l'état.
Les Queries sont sans effet de bord.
Les communications temps réel utilisent AsyncAPI.
29. Critères d'acceptation

L'architecture de communication est considérée conforme lorsque :

toutes les interfaces sont documentées ;
les contrats sont versionnés ;
les tests de contrat sont automatisés ;
les événements sont compatibles entre versions ;
les SDK peuvent être générés automatiquement à partir des spécifications.
🏛️ Décision d'architecture majeure : Contract-Driven Platform (CDP)

Je recommande d'adopter officiellement une approche Contract-Driven Platform.

Avant toute implémentation :

le contrat est défini ;
les schémas sont validés ;
les tests de contrat sont écrits ;
seulement ensuite, les producteurs et consommateurs sont développés.

Ainsi, les équipes Backend, Frontend, IA et QA peuvent travailler en parallèle sur une base contractuelle commune.

📘 Prochaine étape : F3 — PostgreSQL Enterprise Data Model

Le prochain volume décrira l'intégralité du modèle de données de la plateforme :

schéma PostgreSQL complet ;
tables métier ;
Event Store ;
projections CQRS ;
index et stratégies de partitionnement ;
migrations versionnées ;
politiques multi-tenant ;
optimisation des performances ;
stratégie d'archivage et de rétention.

Ce volume servira de référence pour la génération des migrations, des modèles SQLAlchemy et des politiques de gouvernance des données.
