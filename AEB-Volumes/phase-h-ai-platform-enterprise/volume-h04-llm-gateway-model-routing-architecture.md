# Volume H04 — LLM Gateway & Model Routing Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE H — AI PLATFORM ENTERPRISE
Volume H04
LLM Gateway & Model Routing Architecture

Version : 1.0

Statut : Enterprise AI Infrastructure

Criticité : Critique

1. Vision

Le LLM Gateway est la porte d'entrée unique vers tous les modèles IA.

Il fournit une couche d'abstraction entre :

les applications ;
les agents ;
les prompts ;
les fournisseurs de modèles.

Architecture :

Applications

      │

      ▼

Agent Runtime

      │

      ▼

LLM Gateway

      │

 ┌────┼──────────────┐

 ▼    ▼              ▼

Cloud Models   Local Models   Private Models
2. Problème résolu

Architecture naïve :

Application

   ├── OpenAI API
   ├── Anthropic API
   ├── Local Ollama
   ├── Azure Model

Problèmes :

couplage fort ;
changement difficile ;
coûts non maîtrisés ;
absence de gouvernance ;
monitoring fragmenté.

Architecture cible :

Application

↓

LLM Gateway

↓

Model Providers
3. Responsabilités du LLM Gateway

Le Gateway gère :

authentification ;
routage ;
quotas ;
sécurité ;
observabilité ;
fallback ;
transformation des requêtes ;
contrôle coûts.
4. Architecture interne
                Request

                   │

                   ▼

          Request Validator

                   │

                   ▼

          Policy Engine

                   │

                   ▼

          Model Router

                   │

                   ▼

          Provider Adapter

                   │

                   ▼

              LLM Model

                   │

                   ▼

          Response Processor

                   │

                   ▼

              Application
5. Provider Adapter Pattern

Chaque fournisseur possède un adaptateur.

Exemple :

providers/

 ├── openai/

 ├── anthropic/

 ├── google/

 ├── azure/

 ├── ollama/

 └── vllm/

Le reste du système ne connaît jamais le fournisseur réel.

6. Interface commune

Tous les modèles exposent une interface uniforme.

Exemple :

class LLMProvider:

    def generate(
        self,
        messages,
        parameters
    ):
        pass
7. Model Registry

Le Gateway utilise un catalogue de modèles.

Exemple :

model:

id:
gpt-enterprise-large


provider:
cloud_provider


capabilities:

- reasoning
- roleplay
- long_context


latency:
medium


cost:
high


privacy:
external
8. Classification des modèles

La plateforme distingue :

Premium Reasoning Models

Utilisés pour :

scénarios complexes ;
évaluations ;
génération pédagogique.
Fast Conversation Models

Utilisés pour :

chat temps réel ;
voix ;
simulations longues.
Local Models

Utilisés pour :

données sensibles ;
classification ;
tâches simples.
9. Model Capability Matrix

Exemple :

Modèle	Latence	Coût	Raisonnement	Voix
Premium LLM	Moyen	Élevé	Très fort	Oui
Fast LLM	Faible	Moyen	Moyen	Oui
Local LLM	Très faible coût	Faible	Variable	Oui
10. Intelligent Model Router

Le Router choisit automatiquement le modèle.

Entrées :

{
"task":
"customer_simulation",

"latency_requirement":
"realtime",

"privacy":
"standard",

"budget":
"medium"
}

Sortie :

{
"selected_model":
"fast-conversation-model",

"reason":

"low latency required"
}
11. Règles de routage

Exemples :

Simulation voix temps réel

Priorité :

Latence
Stabilité
Coût
Evaluation QA

Priorité :

Raisonnement
Qualité
Coût
Données sensibles

Priorité :

Confidentialité
Localisation
Sécurité
12. Routing Policy Engine

Les règles sont déclaratives.

Exemple :

policy:

task:
voice_training


constraints:

max_latency_ms:
500


preferred_models:

- fast_model

fallback:

- local_model
13. Fallback Strategy

Un modèle peut être indisponible.

Architecture :

Primary Model

       ↓

Failure

       ↓

Fallback Model

       ↓

Local Backup

       ↓

Error Handling
14. Retry Strategy

Le Gateway gère :

timeout ;
erreur réseau ;
surcharge ;
limite fournisseur.

Exemple :

retry:

max_attempts:
3

backoff:
exponential
15. Streaming Architecture

Pour la voix et le chat temps réel :

User

↓

Streaming Gateway

↓

LLM Stream

↓

Token Events

↓

Client

Événements :

{
"type":
"token",

"value":
"Bonjour"
}
16. Gestion du contexte

Le Gateway ne stocke pas toute la mémoire.

Il reçoit :

{
"messages":
[],

"context_id":
"SESSION-9912"
}

La mémoire reste dans :

Memory Engine

17. Sécurité

Le Gateway applique :

Input Controls
détection injection ;
validation format ;
filtrage données sensibles.
Output Controls
validation réponse ;
contrôle format ;
détection fuite information.
18. Tenant Isolation

Chaque appel porte :

{
"tenant_id":
"enterprise_001",

"policy":
"private_only"
}

Le Gateway applique les règles du tenant.

19. Cost Management

Chaque appel produit :

{
"tenant":
"company_A",

"model":
"premium",

"tokens":
4500,

"estimated_cost":
"tracked"
}
20. Budget Guardrails

Exemple :

tenant_budget:

monthly_limit:
configured


actions:

warning:
80%

block:
100%
21. LLM Gateway API

Exemple :

POST /v1/generate

Payload :

{
"agent_id":
"customer_persona",

"prompt_id":
"persona_v3",

"task":
"conversation",

"requirements":

{
"latency":
"low"
}
}

Réponse :

{
"model":
"fast-model",

"response":
"Bonjour",

"latency_ms":
320
}
22. Observabilité

Chaque appel produit un événement :

{
"request_id":
"REQ-888",

"model":
"model_x",

"tokens_input":
2000,

"tokens_output":
500,

"latency":
700,

"success":
true
}
23. Data Model
Model Entity
Model
-----

id

provider

name

capabilities

cost_profile

privacy_level

status
LLM Request
LLMRequest
----------

id

tenant_id

agent_id

model_id

tokens

latency

status

created_at
24. Décisions d'architecture (ADR)
ADR-H04-001
Aucun service applicatif ne contacte directement un LLM.

Décision :

Tous les appels passent par le Gateway.

ADR-H04-002
Le choix du modèle est dynamique.

Décision :

Le modèle est une décision runtime.

ADR-H04-003
Les politiques de routage sont configurables.

Décision :

Pas de logique métier codée en dur.

ADR-H04-004
Le coût IA est une métrique de premier niveau.

Décision :

Chaque utilisation doit être attribuable.

25. Critères d'acceptation

Le LLM Gateway est conforme lorsque :

✅ plusieurs fournisseurs peuvent être intégrés ;

✅ un modèle peut être remplacé sans modifier les applications ;

✅ le routage automatique fonctionne ;

✅ les coûts sont suivis ;

✅ les appels sont observables ;

✅ les politiques tenant sont respectées ;

✅ les fallback fonctionnent.

🏛️ Décision d'architecture majeure : Enterprise LLM Control Plane Architecture (ELCPA)

Je recommande une architecture :

Enterprise LLM Control Plane

Le LLM Gateway devient le plan de contrôle IA de l'entreprise.

Son rôle n'est pas uniquement de transporter des requêtes.

Il gouverne :

quel modèle est utilisé ;
pourquoi il est utilisé ;
combien il coûte ;
dans quel contexte ;
avec quelles restrictions.

Il devient l'équivalent d'un :

API Gateway pour les services ;
Kubernetes Control Plane pour les workloads ;
MLOps Registry pour les modèles.
📘 État d'avancement
Phase H — AI Platform Enterprise

Terminé :

✅ H01 — AI Platform Core Architecture
✅ H02 — Agent Runtime Architecture
✅ H03 — Prompt Engineering Platform
✅ H04 — LLM Gateway & Model Routing

Restants :

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

Volume H05 — Memory & Context Architecture

Ce volume définira le système mémoire complet de la plateforme :

mémoire court terme ;
mémoire session ;
mémoire long terme ;
mémoire métier ;
mémoire vectorielle ;
stratégie RAG ;
gestion du contexte ;
compression mémoire ;
isolation multi-tenant.
