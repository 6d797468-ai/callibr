# Volume C05 — Runtime Infrastructure, Platform Engineering & Cloud Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE C — PLATFORM CORE ARCHITECTURE
Volume C5
Runtime Infrastructure, Platform Engineering & Cloud Architecture

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

ATOS est conçu selon une architecture Cloud Native, mais sans dépendre d'un fournisseur de cloud particulier.

Le système doit pouvoir être exécuté sur :

Docker Compose (développement)
Kubernetes (production)
Bare Metal
Machines Virtuelles
Cloud public
Cloud privé
Edge Computing (optionnel)

L'infrastructure est décrite comme du code (Infrastructure as Code).

2. Architecture globale
                    Internet

                        │

                CDN / Reverse Proxy

                        │

                API Gateway / Ingress

                        │

        ┌───────────────┼────────────────┐

        ▼               ▼                ▼

   Frontend         REST API        WebSocket API

                        │

                    Kernel

                        │

        ┌───────────────┼────────────────┐

        ▼               ▼                ▼

   Simulation      Conversation       CRM Engine

        ▼               ▼                ▼

     Event Bus      Background Workers  Scheduler

                        │

        ┌───────────────┼────────────────┐

        ▼               ▼                ▼

 PostgreSQL         Redis         Object Storage

                        │

                    Observability
3. Architecture physique

Le système est composé de plusieurs services.

Gateway

API

Kernel

Workers

Scheduler

Event Bus

PostgreSQL

Redis

Object Storage

Monitoring

Logging

Chaque composant est déployable indépendamment.

4. Services Python

Je recommande les services suivants.

atos-api

atos-kernel

atos-worker

atos-scheduler

atos-events

atos-auth

atos-notification

atos-reporting

Chaque service possède son propre cycle de vie.

5. Runtime Python

Recommandations.

Élément	Choix
Python	3.13+
Framework	FastAPI
ORM	SQLAlchemy 2.x
Validation	Pydantic v2
Migrations	Alembic
Async	asyncio
HTTP	httpx
WebSocket	Starlette
6. Conteneurs

Chaque composant est conteneurisé.

Frontend

↓

Image Docker

API

↓

Image Docker

Workers

↓

Image Docker

Les images sont immuables.

7. Kubernetes

Déploiement recommandé.

Namespace

↓

Deployment

↓

ReplicaSet

↓

Pods

Chaque moteur peut être répliqué horizontalement.

8. Autoscaling

Le système adapte automatiquement.

Selon.

CPU
RAM
nombre de sessions
longueur des files
appels LLM
trafic WebSocket
9. Workers

Les traitements longs sont externalisés.

Exemples.

Evaluation QA

↓

Worker
Rapport PDF

↓

Worker
Import Scénarios

↓

Worker

Les API restent réactives.

10. Scheduler

Le Scheduler exécute.

rappels ;
nettoyage ;
exports ;
snapshots ;
sauvegardes ;
recalculs ;
maintenance.
11. Stockage

Trois catégories.

Relationnel

PostgreSQL.

Cache

Redis.

Fichiers

Object Storage compatible S3.

Exemples.

MinIO
AWS S3
Azure Blob
Google Cloud Storage
12. Gestion des secrets

Aucun secret dans Git.

Utiliser.

Kubernetes Secrets
HashiCorp Vault
AWS Secrets Manager
Azure Key Vault

Rotation automatique recommandée.

13. Configuration

Hiérarchie.

Default

↓

Environment

↓

Tenant

↓

Workspace

La surcharge est contrôlée.

14. Observabilité

Trois piliers.

Logs

Metrics

Traces

Tous les services doivent exposer ces trois dimensions.

15. Logs

Logs JSON structurés.

Exemple.

{
  "timestamp": "...",
  "service": "atos-api",
  "tenant": "tenant-01",
  "trace_id": "...",
  "level": "INFO",
  "message": "Simulation started"
}

Les logs ne contiennent jamais de données sensibles.

16. Metrics

Prometheus collecte.

CPU
RAM
latence
temps LLM
temps CRM
erreurs
taux de succès
événements/seconde
17. Tracing

OpenTelemetry est utilisé.

Propagation.

Gateway

↓

API

↓

Kernel

↓

Worker

↓

Database

Une seule Trace ID.

18. Dashboards

Grafana fournit.

Infrastructure
API
IA
LLM
CRM
QA
Analytics
19. Alerting

Alertes automatiques.

Exemples.

CPU > 80 %
erreur > 5 %
LLM indisponible
Event Bus saturé
PostgreSQL en retard
Redis indisponible
20. Sauvegardes

Plan recommandé.

Composant	Fréquence
PostgreSQL	Quotidienne
Event Store	Continue
Stockage objet	Quotidien
Configurations	À chaque changement

Des tests de restauration sont exécutés régulièrement.

21. Haute disponibilité (HA)

Les composants critiques sont répliqués.

API
Gateway
Workers
Redis Sentinel ou Cluster
PostgreSQL HA
Event Bus

Aucun point unique de défaillance en production.

22. Reprise après sinistre (DR)

Objectifs.

Indicateur	Cible
RPO	< 5 minutes
RTO	< 30 minutes

Ces objectifs sont ajustables selon le contrat client.

23. CI/CD

Pipeline recommandé.

Commit

↓

Lint

↓

Tests unitaires

↓

Tests d'intégration

↓

Analyse sécurité

↓

Build Docker

↓

Scan image

↓

Déploiement Staging

↓

Tests E2E

↓

Validation

↓

Production

Aucun déploiement manuel en production.

24. Sécurité de la chaîne logicielle

Le pipeline inclut.

SBOM (Software Bill of Materials)
signature des images
scan des dépendances
scan des conteneurs
vérification des licences
politiques de déploiement
25. Environnements
Local

↓

Development

↓

Continuous Integration

↓

Staging

↓

Pre-Production

↓

Production

Chaque environnement est isolé.

26. Gestion des versions

Versionnement sémantique.

Exemple.

1.8.0
MAJOR : rupture de contrat
MINOR : nouvelles fonctionnalités compatibles
PATCH : corrections

Les APIs et les événements suivent également ce principe.

27. Stratégie de déploiement

Support des stratégies suivantes.

Rolling Update
Blue/Green
Canary
Feature Flags

Les fonctionnalités IA peuvent être activées progressivement.

28. Performance

Objectifs initiaux (MVP SaaS).

Indicateur	Objectif
Temps de réponse API	< 200 ms (hors LLM)
Latence WebSocket	< 100 ms
Temps de démarrage d'une simulation	< 2 s
Disponibilité	99,9 %
Création d'un rapport QA	< 10 s

Ces objectifs seront réévalués selon les usages réels.

29. Décisions d'architecture (ADR)

Ce volume fixe les décisions suivantes :

Cloud Native et Cloud Agnostic.
Tous les services sont conteneurisés.
Les traitements longs sont asynchrones.
Observabilité native avec OpenTelemetry.
Déploiement automatisé via CI/CD.
Stockage objet compatible S3.
Infrastructure décrite comme du code.
Haute disponibilité prévue dès l'architecture.
30. Critères d'acceptation

L'infrastructure sera considérée conforme lorsque :

la plateforme peut être déployée avec Docker Compose en développement ;
le même code fonctionne sur Kubernetes sans modification métier ;
tous les services exposent des métriques, logs et traces ;
les sauvegardes et restaurations sont testées ;
les déploiements sont automatisés ;
la montée en charge horizontale est démontrée.
🏛️ Décision d'architecture majeure : Platform Engineering & GitOps

Pour les versions Enterprise, je recommande d'adopter une approche GitOps.

Toutes les ressources de la plateforme deviennent déclaratives :

Infrastructure (Terraform)
Kubernetes (Helm/Kustomize)
Configurations (YAML)
Domain Packs
Politiques de sécurité
Déploiements
Observabilité

Le dépôt Git devient la source de vérité de la plateforme.

Les avantages sont :

déploiements reproductibles ;
audit complet des changements ;
restauration simplifiée ;
validation automatisée des configurations ;
gouvernance renforcée.
📚 Fin de la Phase C — Bilan

La Phase C établit le socle technique d'ATOS :

C1 : Micro-Kernel & Architecture Hexagonale
C2 : Event Sourcing, CQRS & Event Bus
C3 : Architecture SaaS Multi-Tenant Enterprise
C4 : API Gateway, SDK & Plateforme d'intégration
C5 : Infrastructure Runtime, Observabilité & Cloud Engineering

Cette phase fournit une architecture robuste, évolutive et adaptée à une plateforme SaaS d'entraînement IA.

Prochaine phase : Phase D — Engineering Standards & Implementation Blueprint

Nous passerons de l'architecture à l'implémentation concrète, avec notamment :

D1 — Monorepo, organisation du code et conventions Python
D2 — Standards de développement et qualité (typing, tests, linting, ADR, CI)
D3 — Blueprint détaillé des Engines (interfaces, packages, classes)
D4 — Stratégie LLM Engineering & Prompt Orchestration
D5 — Plan de développement itératif (MVP → Enterprise)
D6 — Prompt directeur pour OpenCode, destiné à piloter le développement du projet jusqu'à la production, en appliquant toutes les décisions architecturales définies dans cet Architecture & Engineering Book.
