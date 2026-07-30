# Volume F03 — PostgreSQL Enterprise Data Model

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE F — DELIVERY, IMPLEMENTATION & ENTERPRISE OPERATIONS
Volume F3
PostgreSQL Enterprise Data Model

Version : 1.0

Statut : Référence d'implémentation

Criticité : Critique

1. Vision

La base PostgreSQL n'est pas uniquement un stockage.

Elle supporte simultanément :

le transactionnel (OLTP) ;
l'historique métier ;
l'Event Store ;
les projections CQRS ;
les statistiques opérationnelles.

Chaque donnée possède un propriétaire, un cycle de vie et une stratégie de rétention.

2. Architecture logique
                    PostgreSQL Cluster

                           │

      ┌────────────────────┼────────────────────┐

      ▼                    ▼                    ▼

 Transaction DB       Event Store        Read Models

      ▼                    ▼                    ▼

 Configurations      Audit Trail       Analytics Cache
3. Principes
UUID v7 pour toutes les clés primaires.
UTC pour toutes les dates.
Soft Delete lorsque nécessaire.
Multi-tenant natif.
Optimistic Locking (version).
Audit systématique.
4. Découpage par schémas
core
identity
training
conversation
crm
evaluation
analytics
knowledge
runtime
audit
reporting
platform

Chaque domaine reste isolé.

5. Tables Platform
tenants

workspaces

users

roles

permissions

api_keys

settings

feature_flags
6. Tables Formation
training_programs

training_modules

training_paths

lessons

exercises

sessions

session_attempts
7. Tables Conversation
scenarios

scenario_versions

personas

conversation_sessions

conversation_messages

conversation_states

emotion_states

conversation_timelines
8. Tables CRM simulé
customers

customer_profiles

contracts

subscriptions

orders

tickets

payments

notes

crm_actions

Ces tables sont purement fictives mais réalistes.

9. Tables Évaluation
evaluations

evaluation_scores

evaluation_rules

qa_forms

feedback

recommendations

coach_reports
10. Tables Analytics
daily_metrics

tenant_metrics

agent_metrics

scenario_metrics

llm_metrics

cost_metrics
11. Tables IA
prompt_templates

prompt_versions

prompt_variables

prompt_executions

model_registry

model_versions

embedding_jobs
12. Tables Knowledge
documents

document_versions

chunks

embeddings

knowledge_links

knowledge_tags
13. Event Store

Une seule table d'événements.

events

Structure :

event_id

aggregate_id

aggregate_type

event_type

version

occurred_at

tenant_id

payload JSONB

metadata JSONB

Cette table est append-only.

14. Read Models

Les projections sont matérialisées.

Exemples :

session_summary

conversation_dashboard

evaluation_dashboard

analytics_dashboard
15. Table Scenarios
scenario_id

domain

difficulty

language

status

current_version

created_by

created_at
16. Scenario Version

Chaque scénario est versionné.

scenario_version_id

scenario_id

semantic_version

json_definition

published

created_at

Le contenu est stocké en JSONB.

17. Persona
persona_id

name

profile

difficulty

emotion_profile

behavior_profile

configuration JSONB
18. Conversation Session
session_id

tenant_id

scenario_version

agent_id

persona_id

status

started_at

ended_at

overall_score
19. Conversation Message
message_id

session_id

sender

sequence

content

token_count

latency_ms

created_at
20. CRM Action

Chaque action effectuée.

action_id

session_id

action_type

payload

result

created_at

Ces actions sont utilisées pendant l'évaluation.

21. Emotion State

Historique.

emotion_state_id

session_id

emotion

patience

confidence

anger

trust

updated_at

On conserve l'évolution.

22. Evaluation
evaluation_id

session_id

score

grade

passed

feedback

created_at
23. Score détaillé
evaluation_scores

criterion

score

weight

comment

Chaque critère est indépendant.

24. Prompt Execution

Historique.

execution_id

provider

model

prompt_version

tokens_input

tokens_output

latency

cost

Ces données alimentent le FinOps IA.

25. Document
document_id

type

version

status

owner

checksum
26. Chunk
chunk_id

document_id

embedding_id

content

metadata

hash
27. Embedding
embedding_id

provider

model

dimension

vector

created_at

Le stockage des vecteurs peut rester dans PostgreSQL (via pgvector) pour le MVP.

28. Audit

Chaque modification critique génère un enregistrement.

audit_id

user_id

action

resource

before

after

timestamp

L'audit est immuable.

29. Multi-tenant

Toutes les tables métier incluent :

tenant_id

Les stratégies recommandées sont :

MVP : Row Level Security (RLS) avec un schéma partagé.
Enterprise : possibilité d'évoluer vers une isolation par base de données pour les clients ayant des exigences fortes de conformité.
30. Indexation

Exemples :

(tenant_id, created_at)
(session_id, sequence)
(scenario_id, semantic_version)
(aggregate_id, version)
index GIN sur JSONB ;
index pgvector pour les embeddings.
31. Partitionnement

À partir d'un certain volume :

conversation_messages
events
audit
prompt_executions

peuvent être partitionnées par mois ou par trimestre selon les volumes observés.

32. Rétention

Politique indicative :

Donnée	Rétention
Messages	Configurable par tenant
Logs techniques	30 à 90 jours
Audit	Longue durée selon conformité
Événements	Conservation métier
Benchmarks	Permanente
33. Migrations

Toutes les évolutions passent par des migrations versionnées.

Convention :

V0001

V0002

V0003

Les migrations sont :

atomiques ;
reproductibles ;
testées automatiquement.
34. Sauvegardes

Politique recommandée :

sauvegarde quotidienne complète ;
sauvegardes incrémentales fréquentes ;
restauration testée régulièrement ;
chiffrement des sauvegardes.
35. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

PostgreSQL est la source de vérité transactionnelle.
L'Event Store est intégré dans PostgreSQL.
Les scénarios, personas et prompts sont versionnés.
Les configurations dynamiques utilisent JSONB.
Les projections CQRS sont séparées des écritures.
Toutes les données métier sont multi-tenant.
36. Critères d'acceptation

Le modèle de données est considéré conforme lorsque :

chaque domaine possède son schéma logique ;
les agrégats métier sont clairement identifiés ;
les événements sont historisés ;
les projections sont indépendantes ;
les migrations sont reproductibles ;
les politiques d'indexation, de sauvegarde et de rétention sont documentées.
🏛️ Décision d'architecture majeure : Hybrid Relational + Event Architecture

Je recommande officiellement une architecture Hybrid Relational + Event Architecture.

Plutôt que d'introduire dès le départ plusieurs technologies spécialisées (base relationnelle, Event Store dédié, moteur de recherche distinct), le MVP s'appuie sur PostgreSQL enrichi avec :

JSONB pour les configurations ;
pgvector pour les embeddings ;
un Event Store append-only ;
des Read Models CQRS.

Cette approche réduit la complexité opérationnelle tout en laissant la possibilité d'extraire certains composants (Event Store, moteur vectoriel, analytique) vers des services dédiés lorsque les besoins de montée en charge le justifieront.

📘 Prochaine étape : F4 — Frontend Architecture & Design System

Le prochain volume définira l'architecture complète de l'interface utilisateur :

structure Next.js ;
App Router ;
organisation des pages ;
Design System ;
composants réutilisables ;
gestion d'état ;
WebSocket temps réel ;
interface de simulation ;
CRM fictif ;
tableau de bord du formateur ;
accessibilité et internationalisation.

Ce document servira de référence pour construire une interface cohérente, modulaire et directement exploitable par OpenCode pour générer les composants Frontend.
