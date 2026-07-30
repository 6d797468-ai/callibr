# Volume F05 — Implementation Roadmap & Sprint Execution Plan

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE F — DELIVERY, IMPLEMENTATION & ENTERPRISE OPERATIONS
Volume F5
Implementation Roadmap & Sprint Execution Plan

Version : 1.0

Statut : Roadmap d'implémentation

Criticité : Critique

1. Vision

ATOS sera développé selon une approche Capability Driven Delivery.

On ne livre pas des composants.

On livre des capacités métier complètes.

Exemple :

❌ Mauvais

Conversation Engine
CRM
Evaluation
Dashboard

✔ Bon

Simulation SAV complète

→ conversation

→ CRM

→ évaluation

→ dashboard

→ analytics

2. Macro Roadmap
Fondations

↓

Core Platform

↓

Conversation Engine

↓

CRM Simulation

↓

Evaluation

↓

Voice

↓

Analytics

↓

Enterprise

↓

Production
3. Phases
Phase	Objectif
P0	Bootstrap
P1	Core Platform
P2	Simulation MVP
P3	Multi-domain
P4	Enterprise
P5	Production Scale
PHASE P0

Bootstrap

Sprint 0

Objectif :

Créer les fondations.

Livrables.

Monorepo
Docker
PostgreSQL
Redis
FastAPI
Next.js
CI
CD
Ruff
Pytest
OpenAPI
Auth minimale

Critère.

Application démarre en local.
Sprint 1

Kernel

Livrables.

Event Bus
Command Bus
Query Bus
Storage
Config
Logger

Critère.

Le Kernel fonctionne.

Sprint 2

Identity

Livrables.

JWT
OAuth
RBAC
Multi-tenant

Critère.

Connexion opérationnelle.

PHASE P1

Conversation Platform

Sprint 3

Conversation Engine

Livrables.

Session
Messages
Timeline
Persona

Critère.

Une conversation fonctionne.

Sprint 4

Scenario Engine

Livrables.

CRUD
Versioning
JSON
Validation

Critère.

Création d'un scénario.

Sprint 5

Persona Engine

Livrables.

Personnalités
Émotions
Patience
Profils

Critère.

Le client IA change de comportement.

PHASE P2

Simulation

Sprint 6

CRM Engine

Livrables.

Recherche client
Vérification identité
Ticket
Historique

Critère.

Le CRM répond.

Sprint 7

Action Engine

Livrables.

VerifyIdentity
CreateTicket
Refund
Discount

Critère.

Les actions impactent la simulation.

Sprint 8

Procedure Engine

Livrables.

Checklist
Obligations
Workflow

Critère.

Les procédures sont suivies.

PHASE P3

Evaluation

Sprint 9

Evaluation Engine

Livrables.

QA
Score
Rapport

Critère.

Une simulation est évaluée.

Sprint 10

Coach Engine

Livrables.

Conseils
Feedback
Recommandations

Critère.

Débriefing généré.

Sprint 11

Analytics

Livrables.

KPIs
Dashboard
Historique

Critère.

Statistiques disponibles.

PHASE P4

Voice

Sprint 12

Voice Runtime

Livrables.

STT
Streaming
TTS

Critère.

Conversation vocale.

Sprint 13

Realtime

Livrables.

WebSocket
Streaming
Notifications

Critère.

Temps réel complet.

Sprint 14

Knowledge

Livrables.

RAG
Documents
Embeddings

Critère.

Le contexte est enrichi.

PHASE P5

Enterprise

Sprint 15

Administration

Livrables.

Tenants
Licences
Audit
Sprint 16

Observabilité

Livrables.

Metrics
Traces
Logs
Sprint 17

LLMOps

Livrables.

AI Gateway
Model Router
Cache
Sprint 18

FinOps

Livrables.

Coûts
Tokens
Quotas
Sprint 19

Sécurité

Livrables.

Audit
Durcissement
Pentest
Sprint 20

Release Candidate

Livrables.

Documentation
Optimisations
Corrections
4. Dépendances
Kernel

↓

Identity

↓

Conversation

↓

Scenario

↓

Persona

↓

CRM

↓

Evaluation

↓

Analytics

↓

Voice

↓

Enterprise

Aucun sprint ne contourne ces dépendances.

5. Définition of Ready (DoR)

Une User Story est prête lorsque :

le besoin métier est décrit ;
les critères d'acceptation sont définis ;
les contrats API existent ;
les impacts sont identifiés ;
les dépendances sont connues.
6. Définition of Done (DoD)

Une fonctionnalité est terminée lorsque :

le code est développé ;
les tests passent ;
la documentation est mise à jour ;
les ADR sont respectées ;
les métriques sont disponibles ;
la revue est validée.
7. Pipeline de livraison
Backlog

↓

Architecture

↓

Specification

↓

Implementation

↓

Review

↓

Tests

↓

Documentation

↓

Benchmark

↓

Release

↓

Monitoring
8. Jalons de validation
Jalon	Validation
Architecture	Principal Architect
Contrats	Platform Architect
Code	Reviewer
Fonctionnel	QA
Métier	Expert Centre de Contacts
IA	AI Quality Framework
Production	Release Manager
9. Gestion des risques

Les risques sont classés :

Architecture
Sécurité
Données
IA
Performance
UX
Déploiement

Chaque Epic possède son registre de risques.

10. Environnements
Local

↓

Development

↓

Integration

↓

Staging

↓

Pre-Production

↓

Production

Chaque promotion est automatisée.

11. Stratégie de livraison

Je recommande :

Sprint : 2 semaines.
Release interne : toutes les 2 semaines.
Release candidate : toutes les 8 semaines.
Version mineure : trimestrielle.
Version majeure : annuelle (ou selon les besoins produit).
12. Métriques de pilotage

Suivi continu de :

vélocité ;
temps de cycle ;
taux de réussite des pipelines ;
couverture de tests ;
dette technique ;
régressions ;
coût IA par sprint.
13. Priorisation

Les Epics sont classés selon :

Valeur métier.
Dépendances techniques.
Réduction des risques.
Impact utilisateur.
Complexité.

Cette priorisation est réévaluée à chaque incrément.

14. Gouvernance des releases

Aucune mise en production sans :

validation des benchmarks IA ;
validation QA ;
revue de sécurité ;
vérification des migrations ;
plan de retour arrière documenté.
15. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Livraison par capacités métier complètes.
Développement incrémental.
Validation continue.
Promotion automatisée entre environnements.
Gouvernance explicite des releases.
16. Critères d'acceptation

La feuille de route est considérée conforme lorsque :

chaque sprint produit une capacité exploitable ;
les dépendances sont respectées ;
les critères DoR/DoD sont appliqués ;
les validations techniques, métier et IA sont réalisées avant chaque promotion.
🏛️ Décision d'architecture majeure : Vertical Slice Delivery

Je recommande officiellement une stratégie de Vertical Slice Delivery.

Chaque incrément traverse toutes les couches :

UX ;
Frontend ;
Backend ;
Domain ;
IA ;
Base de données ;
Tests ;
Documentation.

Cette approche permet de disposer très tôt d'une plateforme fonctionnelle et réduit le risque d'intégration tardive.

📘 Prochaine étape : F6 — Production Runbook & Enterprise Operations

Le prochain volume conclura la Phase F en décrivant l'exploitation en production :

CI/CD GitHub Actions ;
stratégie Docker et Kubernetes ;
déploiements progressifs (Blue/Green, Canary) ;
supervision (OpenTelemetry, Prometheus, Grafana) ;
sauvegardes et restauration ;
PRA/PCA ;
gestion des incidents ;
SRE, SLI/SLO ;
exploitation quotidienne ;
procédures d'urgence et runbooks.

Ce volume constituera le guide opérationnel permettant de faire fonctionner ATOS de manière fiable, sécurisée et observable en environnement de production.
