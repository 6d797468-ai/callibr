# Volume H05 — Memory & Context Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H05
Memory & Context Architecture

Version : 1.0

Statut : Enterprise AI Infrastructure

Criticité : Critique

1. Vision

Le Memory & Context Engine est le système cognitif de la plateforme.

Il fournit aux agents :

continuité ;
historique ;
connaissance ;
compréhension du contexte ;
personnalisation.

Architecture :

                    Agent Runtime

                          │

                          ▼

              Memory & Context Engine

                          │

        ┌─────────────────┼─────────────────┐

        ▼                 ▼                 ▼

 Short Term          Long Term          Knowledge
 Memory              Memory             Memory


        │                 │                 │

        └─────────────────┼─────────────────┘

                          ▼

                     Data Layer
2. Principe fondamental

La mémoire n'est pas unique.

Erreur classique :

Conversation History = Memory

Cette approche ne passe pas à l'échelle.

Une plateforme Enterprise nécessite plusieurs couches.

3. Architecture mémoire multi-couches
Memory Architecture

        │

        ├── Working Memory
        │
        ├── Session Memory
        │
        ├── Episodic Memory
        │
        ├── Semantic Memory
        │
        ├── Business Memory
        │
        └── Knowledge Memory
4. Working Memory
Définition

Mémoire active utilisée pendant une génération.

Durée :

Quelques secondes.

Contient :

derniers messages ;
objectif courant ;
état émotionnel ;
action en cours.

Exemple :

{
"current_goal":
"verify_customer_identity",

"last_message":
"Je souhaite résilier",

"emotion":
{
"anger":35
}
}
5. Session Memory

Mémoire de la simulation actuelle.

Durée :

Une session.

Contient :

conversation complète ;
actions effectuées ;
décisions ;
scores intermédiaires.

Exemple :

{
"session_id":
"SIM-2027-001",

"scenario":
"RET-004",

"steps_completed":

[
"identity_check",
"ticket_created"
]
}
6. Episodic Memory

Mémoire des événements passés.

Elle permet :

analyse historique ;
progression ;
apprentissage.

Exemple :

Un agent humain a déjà échoué sur :

gestion colère client ;
identification ;
procédure remboursement.

La plateforme peut proposer un entraînement ciblé.

7. Semantic Memory

Mémoire des connaissances générales.

Exemples :

procédures ;
FAQ ;
politiques ;
documentation.

Elle est utilisée principalement par :

RAG Engine

8. Business Memory

Mémoire spécifique au métier.

Exemples :

Banque :

Politique crédit
Procédure fraude
Règles conformité

Télécom :

Offres
Incidents réseau
Procédures SAV
9. Knowledge Memory

Stockage documentaire.

Sources :

PDF ;
manuels ;
procédures ;
bases internes ;
scripts.

Pipeline :

Documents

↓

Extraction

↓

Chunking

↓

Embedding

↓

Vector Database

↓

Retrieval
10. Context Builder

Le Context Builder construit le contexte envoyé au LLM.

Entrées :

Current Message

+

Working Memory

+

Session State

+

Relevant History

+

Knowledge Retrieval

+

Business Rules

Sortie :

Optimized Context Window
11. Context Window Management

Problème :

Les modèles ont une limite de contexte.

Une conversation longue ne peut pas être envoyée intégralement.

Solution :

Compression intelligente.

Architecture :

Conversation

↓

Importance Ranking

↓

Summarization

↓

Context Selection

↓

LLM
12. Memory Importance Scoring

Chaque information possède un score.

Exemple :

{
"fact":
"Client refuse toute offre premium",

"importance":
0.92,

"source":
"conversation"
}

Priorité :

règles métier ;
identité ;
décisions ;
préférences ;
historique secondaire.
13. Memory Retrieval Engine

Le moteur récupère uniquement les informations utiles.

Architecture :

Query

↓

Embedding

↓

Vector Search

↓

Filtering

↓

Ranking

↓

Context Injection
14. Recherche hybride

Une architecture Enterprise utilise :

Recherche vectorielle

Pour :

sens ;
similarité.
Recherche classique

Pour :

identifiants ;
références ;
codes.

Architecture :

User Query

      │

      ├── Vector Search

      │

      └── Keyword Search


              ↓

          Fusion Ranking
15. Vector Database

Rôle :

Stocker les représentations sémantiques.

Exemples de technologies :

Qdrant ;
Weaviate ;
Milvus ;
Elasticsearch Vector.

Structure :

{
"id":
"doc_chunk_001",

"embedding":
[0.231,0.551],

"metadata":
{
"tenant":
"company01",

"domain":
"banking"
}
}
16. Isolation Multi-Tenant

La mémoire est strictement séparée.

Interdit :

Tenant A Memory

        ↓

Tenant B Retrieval

Architecture :

Tenant A

Namespace A


Tenant B

Namespace B
17. Memory Security Layer

Contrôles :

permissions ;
chiffrement ;
expiration ;
suppression ;
audit.
18. Memory Lifecycle

Chaque donnée suit un cycle :

Created

↓

Indexed

↓

Used

↓

Updated

↓

Archived

↓

Deleted
19. Memory Expiration Policy

Toutes les mémoires ne vivent pas éternellement.

Exemple :

memory_policy:

session_memory:

retention:
30_days


temporary_context:

retention:
24_hours
20. Memory API

Interface interne :

POST /memory/store

Exemple :

{
"type":
"session",

"session_id":
"SIM-123",

"content":
"Client refuse la solution proposée"
}

Recherche :

POST /memory/search

Réponse :

{
"results":

[
{
"content":
"Client préfère une solution simple",

"score":
0.91
}
]
}
21. Memory Event System

Chaque modification produit un événement.

Exemple :

{
"event":
"memory_created",

"type":
"episodic",

"agent":
"trainer_agent"
}
22. Intégration avec Agent Runtime

Flux complet :

Agent Request

↓

Load Context

↓

Memory Retrieval

↓

Prompt Compilation

↓

LLM

↓

Memory Update

↓

Response
23. Intégration avec RAG

Le RAG devient une capacité de mémoire spécialisée.

Architecture :

Knowledge Base

↓

Embedding Pipeline

↓

Vector Store

↓

Retriever

↓

Context Builder

↓

LLM
24. Data Model
Memory Item
MemoryItem
-----------

id

tenant_id

agent_id

session_id

type

content

importance_score

created_at

expires_at
Memory Vector
MemoryVector
------------

id

memory_id

embedding

metadata
25. Décisions d'architecture (ADR)
ADR-H05-001
La mémoire est composée de plusieurs couches.

Décision :

Aucune mémoire unique ne doit gérer tous les usages.

ADR-H05-002
Le contexte envoyé au LLM est construit dynamiquement.

Décision :

L'historique complet n'est jamais envoyé systématiquement.

ADR-H05-003
La mémoire est isolée par tenant.

Décision :

Aucune récupération cross-tenant.

ADR-H05-004
Les connaissances métier passent par un mécanisme RAG.

Décision :

Les documents ne sont jamais injectés intégralement dans les prompts.

26. Critères d'acceptation

Le Memory & Context Engine est conforme lorsque :

✅ les différents types de mémoire sont séparés ;

✅ les sessions sont isolées ;

✅ le contexte est optimisé automatiquement ;

✅ les connaissances métier sont accessibles via RAG ;

✅ les données expirent selon des politiques définies ;

✅ toutes les opérations mémoire sont auditables.

🏛️ Décision d'architecture majeure : Cognitive Memory Fabric Architecture (CMFA)

Je recommande une architecture :

Cognitive Memory Fabric Architecture

La mémoire devient une couche transverse comparable à :

un système de fichiers pour un OS ;
un data fabric pour une entreprise ;
un knowledge graph pour une plateforme intelligente.

Les agents ne possèdent pas leur propre mémoire.

Ils consomment une Memory Fabric commune gouvernée.

📘 État d'avancement
Phase H — AI Platform Enterprise

Terminé :

✅ H01 — AI Platform Core Architecture
✅ H02 — Agent Runtime Architecture
✅ H03 — Prompt Engineering Platform
✅ H04 — LLM Gateway & Model Routing
✅ H05 — Memory & Context Architecture

Restants :

H06 — Tool Calling Platform
H07 — Multi-Agent Orchestration
H08 — AI Safety & Guardrails
H09 — Evaluation & Benchmarking Engine
H10 — AI Observability Platform
H11 — Model Registry & MLOps
H12 — AI Cost Optimization
H13 — Enterprise AI Governance
H14 — AI Security Architecture
H15 — Production AI Operations

Prochaine étape :

Volume H06 — Tool Calling Platform Architecture

Ce volume définira la capacité des agents à agir dans des environnements simulés et réels :

définition des outils ;
API Tools ;
Function Calling ;
permissions ;
validation ;
sandbox ;
exécution sécurisée ;
audit des actions.
