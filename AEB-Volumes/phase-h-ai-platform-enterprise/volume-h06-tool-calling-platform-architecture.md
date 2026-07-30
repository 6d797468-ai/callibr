# Volume H06 — Tool Calling Platform Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H06
Tool Calling Platform Architecture

Version : 1.0

Statut : Enterprise AI Action Infrastructure

Criticité : Critique

1. Vision

Le Tool Calling Platform est la couche qui permet aux agents IA d'interagir avec des systèmes externes de manière contrôlée.

Architecture :

                    Agent Runtime

                          │

                          ▼

                 Tool Calling Platform

                          │

        ┌─────────────────┼─────────────────┐

        ▼                 ▼                 ▼

 CRM Tools          Workflow Tools     Knowledge Tools


        │                 │                 │

        ▼                 ▼                 ▼


 Simulation Systems   Business Engines   APIs
2. Principe fondamental
Le LLM ne réalise jamais directement une action.

Architecture interdite :

LLM

↓

UPDATE DATABASE

↓

Modification

Pourquoi ?

absence de contrôle ;
risque de corruption ;
absence d'audit ;
problème de sécurité.

Architecture correcte :

LLM

↓

Tool Request

↓

Tool Runtime

↓

Validation

↓

Execution

↓

Result

↓

LLM
3. Définition d'un Tool

Un Tool est une capacité exposée à un agent.

Un outil possède :

un nom ;
une description ;
un schéma d'entrée ;
un schéma de sortie ;
des permissions ;
des règles d'utilisation.

Exemple :

{
"name":
"crm.get_customer",

"description":
"Retrieve customer information",

"input_schema":

{
"customer_id":
"string"
},

"permissions":

[
"customer_read"
]
}
4. Architecture interne
              Tool Request

                    │

                    ▼

          Tool Permission Layer

                    │

                    ▼

          Schema Validator

                    │

                    ▼

          Tool Executor

                    │

                    ▼

          External Service

                    │

                    ▼

          Result Processor
5. Tool Registry

Comme les prompts et les modèles, les outils doivent être enregistrés.

Le Tool Registry contient :

catalogue des outils ;
versions ;
permissions ;
propriétaires ;
documentation ;
métriques.

Exemple :

tool:

id:
crm_lookup_customer


version:
1.0


category:
crm


owner:
platform_team


status:
production
6. Types de Tools
6.1 Read Tools

Lecture uniquement.

Exemples :

rechercher client ;
consulter commande ;
lire historique.
6.2 Write Tools

Modification contrôlée.

Exemples :

créer ticket ;
ajouter note ;
enregistrer action.
6.3 Workflow Tools

Déclenchent un processus.

Exemples :

lancer retour produit ;
ouvrir escalade ;
démarrer validation.
6.4 Knowledge Tools

Accès aux connaissances.

Exemples :

rechercher procédure ;
trouver article FAQ.
7. Tool Schema Standard

Tous les outils utilisent un format commun.

Exemple :

{
"tool":

{
"name":
"ticket.create",

"parameters":

{
"type":"object",

"properties":

{
"subject":
{
"type":"string"
},

"priority":
{
"type":"string"
}

}

}

}
}
8. Tool Execution Lifecycle

Cycle complet :

Requested

↓

Validated

↓

Authorized

↓

Executed

↓

Result Returned

↓

Logged

↓

Evaluated
9. Permission Model

Chaque agent possède des droits.

Exemple :

agent:

customer_persona:


allowed_tools:

- customer.lookup


denied_tools:

- payment.execute

- customer.delete
10. RBAC + ABAC

La plateforme utilise deux niveaux.

RBAC

Basé sur le rôle.

Exemple :

Trainer Agent

→ accès évaluation
ABAC

Basé sur le contexte.

Exemple :

Agent

peut utiliser

crm.lookup

uniquement si :

tenant = même organisation

session = active
11. Tool Sandbox

Les outils doivent pouvoir fonctionner dans plusieurs environnements.

Exemple :

Development

↓

Sandbox

↓

Staging

↓

Production

Pour la simulation :

CRM réel interdit

↓

CRM Simulator autorisé
12. Tool Result Validation

Les résultats retournés doivent être contrôlés.

Exemple :

Tool :

crm.lookup_customer

Résultat :

{
"name":
"Jean Martin",

"status":
"active"
}

Validation :

format correct ;
permissions respectées ;
données autorisées.
13. Tool Error Handling

Un outil peut échouer.

Cas :

timeout ;
donnée absente ;
permission refusée ;
erreur système.

Flux :

Tool Failure

↓

Retry

↓

Alternative Tool

↓

Human Escalation

↓

Incident Log
14. Tool Chaining

Certains scénarios nécessitent plusieurs actions.

Exemple :

Résiliation abonnement :

verify_identity

↓

get_contract

↓

check_commitment

↓

calculate_refund

↓

create_request

Le Runtime orchestre la chaîne.

15. Tool Planning

L'agent peut déterminer une séquence d'actions.

Mais :

Le plan doit être validé.

Architecture :

LLM

↓

Proposed Plan

↓

Policy Engine

↓

Approved Actions

↓

Execution
16. Human Approval Gate

Certaines actions nécessitent une validation humaine.

Exemple :

Remboursement important

↓

Approval Required

↓

Execution
17. Tool Observability

Chaque action produit un événement.

Exemple :

{
"tool":
"ticket.create",

"agent":
"support_agent",

"duration_ms":
220,

"status":
"success"
}
18. Audit Trail

Toutes les actions sont conservées.

Historique :

Agent

↓

Tool

↓

Parameters

↓

Result

↓

Timestamp
19. Intégration avec les Domain Packs

Exemple SAV :

Persona Client

↓

Agent Runtime

↓

Tool:

crm.lookup_ticket

↓

Ticket Engine

↓

Response

Exemple banque :

Agent

↓

identity.verify

↓

customer.lookup

↓

fraud.check

↓

solution
20. Data Model
Tool Entity
Tool
----

id

name

version

description

schema

permissions

status
Tool Execution
ToolExecution
--------------

id

tool_id

agent_id

session_id

input

output

status

latency

created_at
21. API interne
Liste des outils disponibles
GET /tools

Réponse :

[
{
"name":
"crm.lookup_customer",

"permission":
"customer_read"
}
]
Exécution
POST /tools/execute

Payload :

{
"tool":
"crm.lookup_customer",

"parameters":

{
"id":
"123"
}
}
22. Sécurité avancée

Protection contre :

appels abusifs ;
injection dans les paramètres ;
escalade de privilèges ;
exécution non autorisée.

Contrôles :

validation schéma ;
rate limiting ;
policy engine ;
audit obligatoire.
23. Décisions d'architecture (ADR)
ADR-H06-001
Les agents n'accèdent jamais directement aux systèmes.

Décision :

Toutes les actions passent par Tool Runtime.

ADR-H06-002
Les outils sont versionnés.

Décision :

Une modification d'outil est un changement logiciel.

ADR-H06-003
Chaque action IA est auditable.

Décision :

Aucune exécution silencieuse.

ADR-H06-004
Les permissions sont natives au runtime.

Décision :

La sécurité n'est pas ajoutée après coup.

24. Critères d'acceptation

Le Tool Calling Platform est conforme lorsque :

✅ les agents peuvent utiliser des outils déclaratifs ;

✅ les permissions sont appliquées ;

✅ les actions sont validées ;

✅ les résultats sont contrôlés ;

✅ toutes les exécutions sont tracées ;

✅ les environnements simulation/staging/production sont séparés ;

✅ un nouvel outil peut être ajouté sans modifier le runtime.

🏛️ Décision d'architecture majeure : AI Action Execution Fabric (AAEF)

Je recommande une architecture :

AI Action Execution Fabric

Cette couche devient l'équivalent des drivers et APIs système d'un OS.

Elle fournit aux agents une capacité d'action universelle tout en maintenant :

contrôle ;
sécurité ;
audit ;
gouvernance.

La séparation fondamentale devient :

Agent = Intelligence

Tool Runtime = Action

Business Engine = Décision métier

Database = Source de vérité

Cette séparation est essentielle pour construire une plateforme IA Enterprise fiable.

📘 État d'avancement
Phase H — AI Platform Enterprise

Terminé :

✅ H01 — AI Platform Core Architecture
✅ H02 — Agent Runtime Architecture
✅ H03 — Prompt Engineering Platform
✅ H04 — LLM Gateway & Model Routing
✅ H05 — Memory & Context Architecture
✅ H06 — Tool Calling Platform

Restants :

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

Volume H07 — Multi-Agent Orchestration Architecture

Ce volume définira le système permettant de faire collaborer plusieurs agents IA :

communication agent-agent ;
rôles spécialisés ;
supervision ;
planification ;
coordination ;
résolution de conflits ;
workflows autonomes ;
architectures de type agent swarm contrôlé.
