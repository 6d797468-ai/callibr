# Volume C04 — API Gateway, Integration Platform & SDK

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE C — PLATFORM CORE ARCHITECTURE
Volume C4
API Gateway, Integration Platform & SDK

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

ATOS est une API First Platform.

Toutes les fonctionnalités doivent être disponibles via une API documentée.

Cela garantit que :

le Frontend est un client comme les autres ;
un LMS peut piloter des simulations ;
un CRM peut lancer des scénarios ;
un agent IA peut orchestrer la plateforme ;
une application mobile peut être développée sans modification du backend.
2. Architecture
                 Clients

 Web
 Mobile
 CLI
 SDK Python
 SDK TypeScript
 LMS
 CRM
 AI Agents

        │

        ▼

    API Gateway

        │

 ┌──────┼─────────────────────┐

 ▼      ▼                     ▼

REST   WebSocket        Webhooks

        │

        ▼

Internal Platform API

        │

        ▼

Event Bus

        │

        ▼

Kernel + Engines
3. Les couches

Nous distinguons.

Public API

↓

Gateway

↓

Internal Platform API

↓

Command Bus

↓

Kernel

Les moteurs ne sont jamais exposés directement.

4. REST API

La REST API couvre :

Tenants

Users

Organizations

Projects

Scenarios

Sessions

CRM

Analytics

Reports

Training

Administration

Toutes les ressources suivent les mêmes conventions.

5. Versionnement

Toutes les API sont versionnées.

Exemple.

/api/v1/

↓

/api/v2/

Une version majeure n'introduit jamais de rupture silencieuse.

6. OpenAPI

Toute l'API est décrite.

OpenAPI 3.1

↓

Documentation

↓

SDK

↓

Tests

↓

Mock Server

La spécification est la référence officielle.

7. API Design

Nous adoptons les principes suivants.

Exemple.

GET /sessions
POST /sessions
GET /sessions/{id}
DELETE /sessions/{id}

Pas de verbes dans les URI.

8. Pagination

Toutes les listes utilisent.

limit

cursor

next_cursor

Éviter les offsets pour les gros volumes.

9. Filtrage

Exemple.

GET /sessions

?status=running

&agent=123

&scenario=incident

&from=2026-01-01

Les filtres sont combinables.

10. Recherche

Recherche uniforme.

GET /search

?q=Dupont

Le moteur choisit les ressources concernées.

11. WebSocket

Le WebSocket sert au temps réel.

Exemples.

Conversation

CRM

Evaluation

Voice

Notifications
12. Flux WebSocket
Frontend

↓

Gateway

↓

Session Runtime

↓

Conversation Runtime

↓

Streaming

↓

Frontend

Les événements sont sérialisés au format JSON.

13. Streaming IA

Les réponses du LLM sont diffusées progressivement.

Token

↓

Token

↓

Token

↓

Réponse complète

L'interface reste fluide.

14. Webhooks

Chaque événement important peut déclencher.

SimulationCompleted

↓

Webhook
CertificationGranted

↓

Webhook
UserCreated

↓

Webhook

Les Webhooks sont signés.

15. API Keys

Chaque intégration possède.

API Key

Scopes

Expiration

Rotation

Les clés ne sont jamais stockées en clair.

16. OAuth2 / OIDC

Authentification recommandée.

OIDC

↓

JWT

↓

Gateway

↓

Kernel

Compatible Azure AD, Keycloak, Auth0, Okta, etc.

17. SDK Python

Le SDK Python encapsule l'API.

Exemple.

client.sessions.create(...)

client.crm.search(...)

client.analytics.report(...)

Le développeur ne manipule pas directement HTTP.

18. SDK TypeScript

Même philosophie.

client.sessions.start()

client.scenarios.list()

client.crm.createTicket()

Les SDK sont générés à partir d'OpenAPI.

19. CLI

Une interface en ligne de commande est fournie.

Exemples.

atos login

atos sessions start

atos scenarios import

atos reports export

La CLI réutilise le SDK Python.

20. Internal Platform API

Les moteurs échangent via des contrats internes.

Exemple.

SessionService

↓

ConversationService

↓

CRMService

↓

AnalyticsService

Ces contrats sont stables et versionnés.

21. Intégrations

Les connecteurs sont des adaptateurs.

Exemples.

Salesforce

Zendesk

ServiceNow

Genesys

Twilio

Moodle

Cornerstone

SAP

Power BI

Ils consomment exclusivement les API publiques ou les événements.

22. Rate Limiting

Le Gateway applique des quotas.

Exemple.

100 req/min

Utilisateur
1000 req/min

Tenant

Les limites sont configurables.

23. Résilience

Le Gateway implémente.

retry contrôlé ;
circuit breaker ;
timeout ;
back-pressure ;
protection contre les rafales (burst).
24. Observabilité

Chaque appel est tracé.

Request ID

↓

Trace ID

↓

Tenant

↓

User

↓

Latency

↓

Status Code

Les traces sont propagées jusqu'aux moteurs.

25. Sécurité

Le Gateway vérifie systématiquement :

authentification ;
autorisation ;
quotas ;
validation des schémas ;
limites de taille ;
signatures des Webhooks ;
protection CSRF (si applicable aux interfaces web) ;
politiques CORS.
26. Contrats

Toutes les réponses suivent un format commun.

Exemple.

{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "...",
    "trace_id": "..."
  },
  "errors": []
}

Les erreurs suivent également un schéma versionné (code, message, détails, documentation).

27. GraphQL (Option Enterprise)

L'API REST reste la référence.

Un endpoint GraphQL peut être proposé pour :

tableaux de bord complexes ;
agrégation de données ;
applications internes.

GraphQL ne remplace pas les commandes métier ni le bus d'événements.

28. API as Product

L'API dispose de son propre cycle de vie.

Roadmap
Changelog
Politique de dépréciation
Tests de compatibilité
Contrats de service (SLA)
Documentation interactive
Exemples officiels

L'API est considérée comme un produit à part entière.

29. Décisions d'architecture (ADR)

Ce volume fixe les décisions suivantes :

Architecture API First.
OpenAPI est la source de vérité des contrats REST.
Les SDK sont générés automatiquement.
Les WebSockets sont réservés au temps réel.
Les Webhooks sont signés et versionnés.
Les intégrations utilisent uniquement les interfaces publiques.
Le Gateway centralise sécurité, quotas et observabilité.
30. Critères d'acceptation

La plateforme d'intégration sera considérée conforme lorsque :

toute fonctionnalité est accessible via une API documentée ;
les SDK Python et TypeScript sont générés à partir d'OpenAPI ;
les WebSockets permettent une diffusion temps réel fiable ;
les Webhooks sont sécurisés et rejouables ;
les API sont versionnées sans rupture ;
les connecteurs externes n'accèdent jamais directement aux moteurs ou à la base de données.
🏛️ Décision d'architecture majeure : Headless Platform

À partir de ce volume, je recommande officiellement qu'ATOS soit conçu comme une Headless AI Training Platform.

Concrètement :

le Frontend React/Next.js devient un client parmi d'autres ;
les applications mobiles, les LMS, les CRM, les assistants IA et la CLI utilisent exactement les mêmes API ;
aucun composant d'interface n'est indispensable au fonctionnement du système.

Cette décision présente plusieurs avantages :

développement indépendant du frontend et du backend ;
création facilitée d'applications mobiles ou embarquées ;
intégration native avec des plateformes tierces ;
meilleure testabilité via des tests d'API ;
ouverture vers des cas d'usage futurs (assistants IA autonomes, orchestrateurs, automatisations).
Prochaine étape : C5 — Runtime Infrastructure & Platform Engineering

Ce volume définira l'infrastructure d'exécution de la plateforme :

architecture des services Python ;
workers asynchrones ;
orchestration des tâches ;
cache distribué ;
stockage objet ;
base de données ;
observabilité (OpenTelemetry, Prometheus, Grafana) ;
CI/CD ;
Kubernetes et déploiement cloud ;
stratégie haute disponibilité et reprise après sinistre (HA/DR) ;
environnements (Dev, CI, Staging, Production).

Ce sera le dernier grand volume de la Phase C et la passerelle vers la Phase D, consacrée à l'implémentation détaillée et aux standards de développement.
