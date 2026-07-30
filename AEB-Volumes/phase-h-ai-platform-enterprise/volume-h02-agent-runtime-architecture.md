# Volume H02 — Agent Runtime Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H02
Agent Runtime Architecture

Version : 1.0

Statut : Enterprise Core Runtime

Criticité : Critique

1. Vision

L'Agent Runtime est le moteur d'exécution universel des agents IA de la plateforme.

Il permet d'exécuter différents types d'agents :

Agent Persona Client ;
Agent Formateur ;
Agent Evaluateur QA ;
Agent Coach ;
Agent Superviseur ;
Agent Générateur de scénarios ;
Agent Assistant Administrateur.
2. Position dans l'architecture globale
                         Applications SaaS

                               │

                               ▼

                     AI Platform Runtime

                               │

        ┌──────────────────────┼──────────────────────┐

        ▼                      ▼                      ▼

 Agent Runtime          Prompt Compiler        Memory Engine


        │                      │                      │

        └──────────────────────┼──────────────────────┘

                               ▼

                         LLM Gateway

                               │

                               ▼

                          Models
3. Définition d'un Agent

Un agent n'est pas un prompt.

Un agent est une unité d'exécution autonome possédant :

agent:

id: customer_persona_agent

type: persona

version: 1.0


identity:

name: Marie_Client_Banque


objective:

simulate_customer_behavior


capabilities:

- conversation
- emotion_management
- memory_access
- crm_lookup


constraints:

- never_break_role
- never_reveal_prompt
- respect_scenario_rules
4. Types d'agents supportés
4.1 Persona Agent

Rôle :

Simuler un interlocuteur humain.

Exemple :

client bancaire ;
patient ;
assuré ;
utilisateur mécontent.
4.2 Trainer Agent

Rôle :

Accompagner l'apprenant.

Fonctions :

donner des conseils ;
expliquer les erreurs ;
proposer des exercices.
4.3 QA Evaluator Agent

Rôle :

Analyser une interaction.

Fonctions :

scoring ;
détection des erreurs ;
recommandations.
4.4 Supervisor Agent

Rôle :

Observer plusieurs sessions.

Fonctions :

monitoring ;
alertes ;
analyse globale.
5. Agent Lifecycle Management

Chaque agent possède un cycle de vie.

Created

↓

Configured

↓

Validated

↓

Published

↓

Running

↓

Paused

↓

Archived
6. Agent Definition Registry

Tous les agents sont enregistrés.

Structure :

{
"id":"persona_bank_customer",

"type":"persona",

"version":"2.1",

"tenant":"bank_company",

"status":"active",

"created_at":"2027-01-01"
}
7. Agent Execution Context

Chaque exécution possède son contexte isolé.

Exemple :

{
"agent_id":
"persona_bank_customer",

"session_id":
"SIM-889921",

"scenario_id":
"BANK-005",

"user_id":
"agent_training_44",

"state":
"identity_verification"
}
8. Isolation des Sessions

Principe critique :

Une session = un environnement isolé.

Interdit :

Session A
   |
   └── mémoire
          |
          Session B

Architecture correcte :

Session A

Memory Namespace A


Session B

Memory Namespace B
9. Agent State Machine

Un agent possède un état interne.

Exemple Persona Client :

state:

emotion:

anger:40

patience:70

trust:50


conversation:

phase:
"problem_description"


goal:

"obtain_solution"
10. State Transition Engine

Les transitions sont contrôlées.

Exemple :

Avant :

Patience : 70
Confiance : 50

Agent humain :

écoute active ;
reformulation ;
solution claire.

Après :

Patience : 85
Confiance : 70

Inverse :

Agent humain :

ignore la demande ;
coupe la parole ;
donne une information incorrecte.

Résultat :

Patience : 35
Confiance : 20
11. Agent Decision Loop

Cycle d'exécution :

Input

↓

Context Loading

↓

State Evaluation

↓

Prompt Compilation

↓

LLM Reasoning

↓

Tool Decision

↓

Action Execution

↓

State Update

↓

Response
12. Agent Action Model

Un agent peut produire :

Réponse conversationnelle
{
"type":"message",

"content":
"Je comprends votre problème."
}
Appel outil
{
"type":"tool_call",

"tool":
"crm.get_customer",

"parameters":
{
"id":"12345"
}
}
Événement interne
{
"type":"state_change",

"emotion":
{
"anger":"+10"
}
}
13. Tool Permission System

Chaque agent possède des permissions.

Exemple :

agent:

name:
bank_customer_agent


tools:

allowed:

- customer_lookup

denied:

- payment_execute
- account_modify
14. Agent Memory Interface

L'agent ne manipule jamais directement la mémoire.

Il utilise une interface :

Agent

↓

Memory API

↓

Memory Engine
15. Agent Communication Protocol

Les agents communiquent via des messages structurés.

Format :

{
"from":
"qa_agent",

"to":
"trainer_agent",

"type":
"feedback",

"payload":

{
"issue":
"missing_empathy"
}
}
16. Multi-Agent Runtime

Certains scénarios nécessitent plusieurs agents.

Exemple :

Simulation centre d'appel complexe :

                 Supervisor Agent

                        |

        ┌───────────────┼───────────────┐

        ▼               ▼               ▼

 Customer Agent   CRM Agent       QA Agent

17. Orchestration interne

Le Runtime possède un Scheduler.

Il gère :

activation ;
arrêt ;
priorité ;
concurrence ;
timeout.
18. Gestion des erreurs

Un agent peut échouer.

Cas :

modèle indisponible ;
outil inaccessible ;
contexte incomplet ;
réponse incohérente.

Stratégie :

Error

↓

Retry

↓

Fallback Model

↓

Human Review

↓

Incident Log
19. Observabilité Agent

Chaque agent produit des événements :

{
"agent":
"persona_customer",

"execution_time_ms":
830,

"llm_calls":
2,

"tool_calls":
1,

"state_changes":
3,

"quality":
0.92
}
20. Sécurité Agent

Contrôles :

identité agent ;
permissions ;
isolation mémoire ;
limites d'action ;
validation des outils ;
audit complet.
21. API interne Agent Runtime

Exemple :

Créer une session :

POST /agent-runtime/session

Payload :

{
"agent_id":
"customer_persona",

"scenario_id":
"RET-005",

"tenant_id":
"company01"
}

Réponse :

{
"session_id":
"SESSION-99122",

"status":
"running"
}
22. Décisions d'architecture (ADR)
ADR-H02-001
Un agent est une entité versionnée.

Décision :

Les agents doivent être versionnés comme du logiciel.

ADR-H02-002
Les agents sont stateful.

Décision :

Une simulation réaliste nécessite un état interne persistant.

ADR-H02-003
Les outils sont contrôlés par permission.

Décision :

Aucun agent ne possède un accès illimité.

ADR-H02-004
Les sessions sont totalement isolées.

Décision :

Aucune fuite de contexte entre simulations.

23. Critères d'acceptation

L'Agent Runtime est conforme lorsque :

✅ un agent peut être créé, publié et exécuté ;

✅ plusieurs sessions peuvent fonctionner simultanément ;

✅ chaque session possède son propre état ;

✅ les permissions outils sont appliquées ;

✅ les agents peuvent évoluer sans modifier le moteur ;

✅ toutes les décisions sont observables ;

✅ les erreurs sont récupérables.

🏛️ Décision d'architecture majeure : Agent Operating Runtime Architecture (AORA)

Je recommande une architecture :

Agent Operating Runtime Architecture

L'objectif est de traiter les agents comme des processus logiciels intelligents.

Un agent possède :

une identité ;
un cycle de vie ;
une mémoire ;
des permissions ;
un état ;
des événements ;
une observabilité.

Cette approche évite le piège des "chatbots améliorés" et transforme la plateforme en véritable système d'exploitation d'agents IA.

📘 État d'avancement
Phase H — AI Platform Enterprise

Terminé :

✅ H01 — AI Platform Core Architecture
✅ H02 — Agent Runtime Architecture

Restants :

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

Prochaine étape :

Volume H03 — Prompt Engineering Platform

Ce volume définira le système industriel de gestion des prompts :

Prompt Registry
Prompt Versioning
Prompt Templates
Prompt Compiler avancé
Prompt Testing
Prompt A/B Testing
Prompt Evaluation
Prompt Governance
Prompt Deployment Pipeline

C'est le composant qui transformera les prompts artisanaux en infrastructure logicielle industrialisée.
