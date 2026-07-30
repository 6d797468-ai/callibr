# Volume H01 — AI Platform Core Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H01
AI Platform Core Architecture

Version : 1.0

Statut : Enterprise Foundation

Criticité : Critique

1. Vision

La plateforme AI Core est le système d'exploitation intelligent de toute la solution.

Elle fournit une couche commune utilisée par :

Conversation Engine ;
Persona Engine ;
Simulation Engine ;
QA Engine ;
Learning Engine ;
Domain Packs métier.

Architecture cible :

                    Applications

                         │

        ┌────────────────────────────────┐
        │       AI Platform Core         │
        └────────────────────────────────┘

                         │

 ┌─────────┬─────────┬─────────┬─────────┐

LLM       Agent     Memory    Tools    Safety
Gateway   Runtime  Engine    Runtime  Layer

                         │

              Models / Data / Services
2. Principes architecturaux fondamentaux
Principe 1 — Le LLM n'est jamais le système métier

Erreur classique :

Utilisateur
    ↓
LLM
    ↓
Décision métier

Architecture interdite.

Architecture correcte :

Utilisateur

↓

Agent Runtime

↓

Business Rules Engine

↓

Tools

↓

LLM

Le LLM raisonne et communique.

Les moteurs déterministes décident.

3. Responsabilités de l'AI Platform Core

Le Core fournit :

Composant	Responsabilité
LLM Gateway	Accès aux modèles
Agent Runtime	Exécution des agents
Prompt Compiler	Construction dynamique des prompts
Memory Engine	Gestion mémoire
Tool Runtime	Actions externes
Safety Layer	Sécurité IA
Evaluation Engine	Mesure qualité
Model Registry	Gestion modèles
Observability	Monitoring IA
4. Architecture logique complète
                     Agent Request

                           │

                           ▼

                 Agent Runtime Layer

                           │

                           ▼

                 Prompt Compiler

                           │

        ┌────────────────────────────┐
        │                            │
        ▼                            ▼

 Context Builder              Memory Engine


        │                            │

        └────────────┬───────────────┘

                     ▼

                LLM Gateway

                     │

       ┌─────────────┼─────────────┐

       ▼             ▼             ▼

   GPT Models    Local Models   Open Models


                     │

                     ▼

              Response Processor


                     │

                     ▼

              Tool Runtime


                     │

                     ▼

            Business Systems
5. AI Platform Multi-Tenant

La plateforme est SaaS.

Elle doit supporter :

plusieurs entreprises ;
plusieurs centres de contacts ;
plusieurs programmes de formation ;
plusieurs modèles ;
plusieurs politiques IA.

Architecture :

Tenant A

 ├── Agents
 ├── Prompts
 ├── Scenarios
 ├── Knowledge Base


Tenant B

 ├── Agents
 ├── Prompts
 ├── Scenarios
 ├── Knowledge Base

Isolation obligatoire.

6. AI Tenant Boundary

Chaque requête IA porte un contexte :

{
  "tenant_id": "company_001",
  "organization_id": "contact_center_fr",
  "agent_id": "trainer_045",
  "scenario_id": "BANK-005",
  "session_id": "sess_88921"
}

Ce contexte contrôle :

accès données ;
modèles autorisés ;
prompts ;
coûts ;
logs.
7. LLM Gateway

Le LLM Gateway est une abstraction entre l'application et les modèles.

Objectifs :

changer de modèle sans modifier le code ;
contrôler les coûts ;
appliquer des politiques ;
mesurer les performances.

Architecture :

Application

↓

LLM Gateway

↓

Provider Adapter

↓

Model
8. Support Multi-Modèles

La plateforme doit supporter :

Modèles Cloud

Exemples :

GPT ;
Claude ;
Gemini.
Modèles locaux

Exemples :

Llama ;
Mistral ;
Qwen ;
modèles GGUF.
9. Model Routing Engine

Le système choisit automatiquement le modèle.

Exemple :

task:

conversation_roleplay:
    model: premium_llm

evaluation:
    model: reasoning_llm

classification:
    model: small_fast_llm

summarization:
    model: local_llm
10. Critères de routage

Le Router prend en compte :

coût ;
latence ;
précision ;
confidentialité ;
disponibilité.

Exemple :

Une simulation temps réel voix nécessite :

Latence < 500 ms

Une analyse QA post-appel peut accepter :

Latence = plusieurs secondes
11. Prompt Compiler

Composant stratégique.

Il transforme des éléments métier en prompt final.

Entrées :

Persona

+

Scenario

+

Difficulty

+

Emotion State

+

CRM State

+

Rules

+

Memory

↓

Sortie :

System Prompt complet
12. Architecture Prompt Compiler
Scenario Definition

        +

Persona Template

        +

Business Rules

        +

Safety Rules

        +

Memory

        +

Current State


              ↓


        Prompt Compiler


              ↓


        Runtime Prompt
13. Exemple Prompt Runtime généré
SYSTEM ROLE:

Tu incarnes Marie Dupont,
cliente bancaire fictive.

OBJECTIF:

Tester la capacité de l'agent
à gérer une contestation bancaire.


PERSONNALITE:

- anxieuse
- méfiante
- exigeante


REGLES:

- ne jamais révéler le scénario
- rester dans le rôle
- répondre uniquement selon ton état


ETAT ACTUEL:

Patience:
65%

Confiance:
40%

Etape:
Vérification identité
14. Agent Runtime

L'Agent Runtime est le moteur d'exécution.

Il gère :

cycle de vie agent ;
état ;
outils ;
mémoire ;
décisions ;
événements.
15. Agent State Machine

Un agent n'est pas une simple conversation.

Il possède un état.

Exemple :

{
"state":"waiting_for_identity_check",

"goal":
"validate_customer",

"allowed_actions":
[
"ask_question",
"use_crm_tool"
]
}
16. Memory Engine

La mémoire est séparée en plusieurs couches.

Short Term Memory

Conversation actuelle.

Session Memory

Simulation actuelle.

Long Term Memory

Historique pédagogique.

Knowledge Memory

Documents métier.

17. Tool Runtime

Un agent peut appeler des outils.

Exemple :

Agent IA

↓

CRM Simulator Tool

↓

get_customer()

↓

Résultat

↓

LLM
18. Sécurité fondamentale

Le Tool Runtime impose :

autorisations ;
validation paramètres ;
logs ;
limites.

Un LLM ne peut jamais appeler directement une base critique.

19. Observabilité IA

Chaque appel produit :

{
"model":"gpt-x",

"tokens_input":3200,

"tokens_output":500,

"latency_ms":820,

"tool_calls":3,

"quality_score":0.91
}
20. Métriques AI Platform

KPIs :

Performance
latence ;
disponibilité ;
erreurs.
Coût
coût par session ;
coût par tenant ;
coût par scénario.
Qualité
score IA ;
taux d'échec ;
cohérence persona.
21. Décisions d'architecture (ADR)
ADR-H01-001

Le LLM ne contient aucune logique métier critique.

Décision :

Toute règle métier appartient aux moteurs déterministes.

ADR-H01-002

Tous les appels LLM passent par un Gateway unique.

Décision :

Aucun service applicatif n'appelle directement un fournisseur IA.

ADR-H01-003

Les prompts sont générés dynamiquement.

Décision :

Les prompts statiques sont interdits en production.

ADR-H01-004

Les agents IA sont stateful.

Décision :

Une simulation nécessite un état persistant et observable.

22. Critères d'acceptation

Le AI Platform Core est conforme lorsque :

✅ plusieurs modèles peuvent être utilisés sans modifier les applications ;

✅ les prompts sont générés dynamiquement ;

✅ chaque session possède un état isolé ;

✅ les outils sont sécurisés ;

✅ les appels IA sont observables ;

✅ les coûts sont attribuables par tenant ;

✅ les décisions métier restent hors LLM.

🏛️ Décision d'architecture majeure : AI Operating System Architecture (AI-OSA)

Je recommande une architecture de type :

AI Operating System Architecture

Le rôle de cette couche est comparable à un système d'exploitation :

elle abstrait les modèles ;
elle fournit un runtime aux agents ;
elle gère mémoire et outils ;
elle applique les politiques ;
elle expose des capacités communes aux applications.

Les Domain Packs deviennent alors des applications métier exécutées au-dessus du AI Operating System.

📘 État d'avancement
Architecture & Engineering Book
Phases terminées :

✅ Phase A — Fondations
✅ Phase B — Architecture métier
✅ Phase C — Architecture applicative
✅ Phase D — Runtime & Orchestration
✅ Phase E — Simulation Platform
✅ Phase F — Learning & QA Platform
✅ Phase G — Contact Center Business Packs

Nouvelle phase
Phase H — AI Platform Enterprise

Progression :

⏳ H01 — AI Platform Core Architecture (terminé)

Restent dans la Phase H :

H02 — Agent Runtime Architecture
H03 — Prompt Engineering Platform
H04 — LLM Gateway & Model Routing
H05 — Memory & Context Architecture
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

15 volumes composent la Phase H.

Nous continuerons avec :

Volume H02 — Agent Runtime Architecture

qui est le cœur d'exécution des agents IA de simulation.
