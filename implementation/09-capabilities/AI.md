# CAP-07 — AI Runtime

Mise a jour : 2026-07-28

## Definition

Capacite d'interagir avec des modeles de langage pour generer des reponses client simulees, avec gestion du prompt, du contexte et du cout.

## Stabilite

L'AI runtime est un composant critique. L'interface est stable, les fournisseurs et modeles changent.

## AEB Volumes Concernes

- B03 — AI Runtime Architecture & Prompt Orchestration Engine (POE)
- E01-E06 — AI Engineering
- H01-H15 — AI Platform Enterprise

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| LLM Provider Port | `engines/conversation/` | Stub deterministe |
| Prompt Manager | Planifie | Planifie |
| Context Manager | Planifie | Planifie |
| Cost Tracker | Planifie | Planifie |

## Niveaux De Maturite

| Niveau | Description | Statut |
| --- | --- | --- |
| L0 | Stub deterministe (reponses predefinies) | Actif |
| L1 | Adaptateur LLM simple (un provider) | Planifie |
| L2 | Multi-provider, fallback, cache | Roadmap |
| L3 | LLMOps complet, cost tracking, guardrails | Roadmap |

## Criteres De Stabilite

Une feature AI est terminee quand :

- Le stub deterministe fonctionne en test
- L'adaptateur LLM repond correctement
- Le contexte de conversation est maintenu
- Les erreurs LLM sont gerees proprement
