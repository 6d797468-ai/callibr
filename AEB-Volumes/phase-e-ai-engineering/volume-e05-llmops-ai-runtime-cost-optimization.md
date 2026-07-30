# Volume E05 — LLMOps, AI Runtime & Cost Optimization

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE E — AI ENGINEERING & AUTONOMOUS DEVELOPMENT
Volume E5
LLMOps, AI Runtime & Cost Optimization

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Le système ne dépend jamais d'un modèle unique.

ATOS doit pouvoir :

changer de modèle sans modifier le code métier ;
comparer plusieurs modèles ;
utiliser différents modèles selon les tâches ;
optimiser les coûts ;
garantir une continuité de service.

Le LLM est un Provider, jamais une dépendance directe des Engines.

2. Architecture globale
                 AI Runtime

                      │

          AI Gateway / Router

                      │

     ┌────────────────┼─────────────────┐

     ▼                ▼                 ▼

 OpenAI          Anthropic         Azure OpenAI

     ▼                ▼                 ▼

 Mistral          Ollama            vLLM

     ▼                ▼                 ▼

      Local GPU      Local CPU      Remote Cluster

Tous les Engines communiquent uniquement avec l'AI Gateway.

3. AI Gateway

L'AI Gateway est responsable de :

sélection du modèle ;
authentification ;
cache ;
limitation de débit ;
journalisation ;
observabilité ;
politiques de sécurité ;
repli (fallback).

Les Engines ignorent le fournisseur réel.

4. AI Provider Interface

Tous les fournisseurs implémentent le même contrat.

class AIProvider(Protocol):

    async def chat(...)

    async def embeddings(...)

    async def speech_to_text(...)

    async def text_to_speech(...)

    async def moderation(...)

Cette abstraction facilite le remplacement d'un fournisseur.

5. Sélection dynamique

Le modèle est choisi selon :

type de tâche ;
niveau de criticité ;
latence attendue ;
coût ;
confidentialité ;
taille du contexte.

Exemple :

Tâche	Modèle recommandé
Conversation client	Modèle conversationnel rapide
Évaluation QA	Modèle plus précis
Résumé	Petit modèle économique
Génération de code	Modèle spécialisé code
Embeddings	Modèle dédié embeddings

La table est configurable.

6. AI Policy Engine

Avant chaque appel :

Task

↓

Policy Engine

↓

Model Selection

↓

Execution

Le moteur applique les politiques définies par l'entreprise.

7. Stratégies de repli

En cas d'échec.

GPT

↓

Erreur

↓

Retry

↓

Autre région

↓

Autre Provider

↓

Petit modèle local

↓

Erreur contrôlée

L'utilisateur reçoit une réponse cohérente.

8. Prompt Cache

Le cache fonctionne sur plusieurs niveaux.

Prompt

↓

Hash

↓

Semantic Cache

↓

Provider Cache

↓

Execution

Les requêtes identiques peuvent être évitées.

9. Response Cache

Les réponses déterministes sont mises en cache.

Exemples :

résumé ;
classification ;
extraction.

Les conversations interactives ne le sont généralement pas.

10. Token Budget

Chaque requête possède un budget.

max_input_tokens:

max_output_tokens:

estimated_cost:

priority:

Le budget est vérifié avant l'exécution.

11. Optimisation du contexte

Le Context Builder :

supprime les doublons ;
retire les informations obsolètes ;
résume les historiques trop longs ;
priorise les documents de référence.

Le contexte est optimisé avant d'être envoyé au modèle.

12. Compression

Lorsque le contexte dépasse les limites :

History

↓

Summarizer

↓

Compressed Context

↓

LLM

Cette compression est traçable.

13. Observabilité

Chaque appel IA produit :

durée ;
modèle ;
fournisseur ;
nombre de tokens ;
coût estimé ;
cache utilisé ;
succès ou erreur.

Ces données alimentent les tableaux de bord.

14. Journalisation

Chaque exécution conserve :

request_id:

trace_id:

tenant_id:

provider:

model:

prompt_version:

latency_ms:

input_tokens:

output_tokens:

estimated_cost:

status:

Les prompts eux-mêmes peuvent être masqués ou chiffrés selon les politiques de confidentialité.

15. Évaluation des modèles

Les modèles sont évalués régulièrement selon :

qualité ;
latence ;
coût ;
stabilité ;
conformité.

Les résultats alimentent les règles de sélection.

16. Benchmarks

Chaque modèle est testé sur :

scénarios conversationnels ;
simulations clients ;
évaluation QA ;
résumé ;
classification.

Les jeux de tests sont versionnés.

17. AI Scorecard

Chaque modèle reçoit une fiche.

Critère	Valeur
Latence moyenne	Mesurée
Coût moyen	Mesuré
Taux d'erreur	Mesuré
Qualité métier	Mesurée
Disponibilité	Mesurée

Ces valeurs servent à orienter le routage.

18. Sécurité

Les politiques définissent :

quels tenants peuvent utiliser quels modèles ;
quelles données peuvent sortir de l'entreprise ;
quelles tâches doivent rester sur une infrastructure locale.

Le routage respecte ces contraintes.

19. Confidentialité

Les informations sensibles peuvent être :

supprimées ;
pseudonymisées ;
chiffrées ;
remplacées par des identifiants temporaires.

Le modèle ne reçoit que les données nécessaires.

20. AI Runtime Health

Chaque Provider expose :

READY

DEGRADED

UNAVAILABLE

MAINTENANCE

L'AI Gateway adapte automatiquement le routage.

21. Gestion des coûts

Le système suit notamment :

coût par session ;
coût par tenant ;
coût par scénario ;
coût par modèle ;
coût par utilisateur.

Des alertes peuvent être déclenchées.

22. Quotas

Chaque tenant peut disposer de :

daily_requests:

monthly_tokens:

monthly_budget:

max_parallel_requests:

Les dépassements sont contrôlés.

23. Optimisation continue

Le système ajuste progressivement :

le choix des modèles ;
les budgets de tokens ;
les politiques de cache ;
les stratégies de résumé.

Les changements sont mesurés avant d'être généralisés.

24. Gouvernance des modèles

Chaque modèle est décrit par un manifeste.

model:

provider:

version:

capabilities:

limitations:

recommended_tasks:

context_window:

status:

Les modèles obsolètes sont retirés progressivement.

25. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les Engines ne dépendent jamais directement d'un fournisseur LLM.
Le routage des modèles est centralisé.
Les coûts, performances et qualités sont mesurés.
Les stratégies de repli sont obligatoires.
Les politiques de sécurité s'appliquent aux appels IA.
26. Critères d'acceptation

La plateforme LLMOps est considérée conforme lorsque :

tous les appels passent par l'AI Gateway ;
les modèles sont interchangeables ;
les coûts et les tokens sont suivis ;
les stratégies de repli fonctionnent ;
les tableaux de bord présentent les indicateurs clés ;
les politiques de confidentialité sont respectées.
🏛️ Décision d'architecture majeure : AI Runtime as a Platform (AIRP)

Je recommande de faire de l'AI Runtime un composant de plateforme indépendant.

Il devient un service partagé fournissant :

le routage intelligent des modèles ;
la gestion des coûts ;
l'observabilité ;
les politiques de sécurité ;
la gouvernance des prompts ;
le cache ;
les mécanismes de repli.

Les Engines ne connaissent que des capacités ("générer une réponse", "évaluer une conversation", "créer des embeddings"), jamais les fournisseurs sous-jacents.

Cette séparation garantit l'évolutivité et facilite l'adoption de nouveaux modèles.

📘 Prochaine étape : E6 — AI Validation, Benchmarking & Continuous Improvement

Ce dernier volume de la Phase E décrira comment valider de manière continue la qualité de l'IA :

framework d'évaluation des scénarios de simulation ;
jeux de tests de référence (golden datasets) ;
benchmarks comparatifs entre modèles ;
détection des régressions ;
A/B testing des prompts et des modèles ;
validation métier avec les équipes QA ;
indicateurs de qualité de simulation et de coaching.

Il clôturera la Phase E en définissant un cycle complet d'amélioration continue, garantissant que la qualité de la plateforme progresse au fil des versions sans régression fonctionnelle ni métier.
