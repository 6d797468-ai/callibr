# Volume E04 — Engineering Knowledge Base & RAG Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE E — AI ENGINEERING & AUTONOMOUS DEVELOPMENT
Volume E4
Engineering Knowledge Base & RAG Architecture

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

L'IA ne doit jamais développer uniquement à partir du code.

Elle doit raisonner à partir des connaissances officielles du projet.

Le code devient une conséquence.

La connaissance devient la source de vérité.

2. Les sources de vérité

Toutes les connaissances ne se valent pas.

ATOS définit une hiérarchie.

Vision Produit

↓

Architecture Book

↓

ADR

↓

Domain Specifications

↓

Contracts

↓

OpenAPI

↓

Schema Database

↓

README

↓

Code

↓

Tests

↓

Issues

Le code n'est pas le premier niveau.

3. Architecture EKOS
Git Repository
      │
      ▼
Document Parser
      │
      ▼
Knowledge Extractor
      │
      ▼
Chunk Builder
      │
      ▼
Embedding Pipeline
      │
      ▼
Vector Store
      │
      ▼
Knowledge API
      │
      ▼
Context Builder
      │
      ▼
OpenCode
4. Types de documents

Le système indexe.

Architecture Book

ADR

README

OpenAPI

Markdown

Python

YAML

JSON

SQL

Diagrammes

Tests

Glossaire

Chaque type possède son analyseur.

5. Granularité

Nous n'indexons jamais un fichier entier.

Nous indexons des unités.

Exemple.

ADR-021

↓

Chunk
README Conversation Engine

↓

Chunk
Interface LLMProvider

↓

Chunk

Les unités restent petites et cohérentes.

6. Métadonnées

Chaque chunk possède.

id:

title:

source:

document_type:

version:

engine:

domain:

author:

updated_at:

tags:

dependencies:

Ces métadonnées servent au filtrage.

7. Indexation

Les index sont organisés.

Architecture

↓

Engineering

↓

Code

↓

Tests

↓

Documentation

↓

Business

Une requête peut cibler un ou plusieurs index.

8. Versionnement

Chaque document possède.

version:

status:

supersedes:

compatible_with:

Les anciennes versions restent consultables.

9. Knowledge Graph

En complément du Vector Store, un graphe relie :

ADR ↔ Engines
Engines ↔ Interfaces
Interfaces ↔ Tests
Tests ↔ User Stories
User Stories ↔ Roadmap

Ce graphe permet des recherches relationnelles.

10. Context Builder

Le Context Builder construit un contexte minimal.

Entrées :

tâche ;
moteur concerné ;
fichiers ;
ADR ;
contrats.

Sortie :

Architecture

↓

Interfaces

↓

Tests

↓

Code utile

L'IA ne reçoit jamais l'intégralité du dépôt.

11. Recherche hybride

Le moteur combine :

recherche sémantique ;
recherche lexicale ;
métadonnées ;
Knowledge Graph.

Cette combinaison réduit les oublis.

12. Politique de priorité

Lorsqu'une information est contradictoire.

Priorité :

ADR

↓

Architecture Book

↓

Contracts

↓

Code

↓

README

↓

Issue

L'IA explique le conflit si nécessaire.

13. Détection d'obsolescence

Le système détecte :

README non synchronisé ;
ADR dépassé ;
contrat non mis à jour ;
documentation incohérente.

Des alertes sont générées.

14. Synchronisation Git

À chaque fusion sur la branche principale :

extraction des changements ;
ré-indexation des documents modifiés ;
mise à jour des embeddings ;
recalcul des liens du graphe.

La base de connaissances reste alignée avec le dépôt.

15. Embeddings

Les embeddings sont générés séparément selon la nature des documents :

documentation ;
code ;
contrats ;
schémas ;
diagrammes.

Cette spécialisation améliore la pertinence des recherches.

16. Knowledge API

L'accès à la connaissance se fait uniquement via une API.

Exemple :

search()

retrieve()

related()

history()

explain()

Les agents IA ne manipulent pas directement le Vector Store.

17. Explicabilité

Chaque réponse du RAG indique :

les documents utilisés ;
leur version ;
leur niveau de priorité ;
leur date.

L'origine des informations est toujours identifiable.

18. Gestion du contexte long

Pour les tâches importantes.

Le contexte est chargé progressivement.

Architecture

↓

Domain

↓

Engine

↓

Task

↓

Code

Cette stratégie limite les coûts et améliore la qualité.

19. Prévention des hallucinations

L'agent ne doit pas inventer.

Si aucune preuve n'est trouvée.

La réponse doit être :

Information non trouvée.

Documents consultés :

...

Recommandation :

Créer une ADR ou compléter la documentation.

L'absence d'information est un résultat valide.

20. Gouvernance documentaire

Chaque document possède :

un propriétaire ;
un statut ;
une version ;
une date de validation.

La documentation devient un actif gouverné.

21. Performance

Objectifs indicatifs :

Indicateur	Cible
Recherche sémantique	< 300 ms
Construction du contexte	< 1 s
Ré-indexation incrémentale	< 30 s
Mise à jour complète	< 15 min

Ces objectifs pourront évoluer selon la taille du dépôt.

22. Sécurité

Les recherches respectent le contexte du demandeur.

Un agent IA ne consulte que les documents autorisés selon :

le tenant ;
le rôle ;
le domaine ;
le niveau de confidentialité.

Le RAG est soumis aux mêmes règles RBAC/ABAC que le reste de la plateforme.

23. Qualité documentaire

Des métriques suivent :

couverture documentaire ;
taux de documents obsolètes ;
liens cassés ;
contradictions détectées ;
documents sans propriétaire.
24. Cycle de vie
Création

↓

Validation

↓

Publication

↓

Indexation

↓

Utilisation

↓

Révision

↓

Archivage

Chaque étape est tracée.

25. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

La documentation est une source de vérité.
Le RAG repose sur une recherche hybride.
Les documents sont découpés en chunks gouvernés.
Le contexte est construit dynamiquement.
Les réponses sont explicables et traçables.
Les informations contradictoires sont signalées.
26. Critères d'acceptation

Le système de connaissance est considéré conforme lorsque :

les documents sont versionnés et indexés ;
les recherches utilisent les métadonnées et le graphe de connaissances ;
le contexte est limité aux informations pertinentes ;
chaque réponse peut citer les documents qui l'ont alimentée ;
la documentation et le dépôt restent synchronisés.
🏛️ Décision d'architecture majeure : Knowledge as Code (KaC)

Je recommande d'adopter officiellement une approche Knowledge as Code.

Au même titre que l'Infrastructure as Code ou la Configuration as Code, la connaissance devient un artefact versionné.

Concrètement :

chaque ADR ;
chaque chapitre de l'Architecture & Engineering Book ;
chaque contrat ;
chaque guide de développement ;
chaque glossaire métier ;

est traité comme un composant du système.

Les modifications suivent les mêmes règles que le code :

revue ;
versionnement ;
validation ;
historique ;
traçabilité.

Cela garantit que la base de connaissances reste fiable, auditable et exploitable par les agents IA.

📘 Prochaine étape : E5 — LLMOps, AI Runtime & Cost Optimization

Ce volume définira l'architecture opérationnelle des modèles d'IA utilisés par ATOS :

gestion de plusieurs fournisseurs (OpenAI, Anthropic, Mistral, Ollama, Azure OpenAI, vLLM) ;
sélection dynamique des modèles selon la tâche ;
cache de prompts et de réponses ;
suivi des coûts et des tokens ;
évaluation continue des modèles ;
stratégies de repli (fallback) ;
optimisation des performances et de la latence ;
gouvernance des modèles et de leurs versions.

Ce document transformera le moteur LLM en un composant piloté, mesuré et optimisé, plutôt qu'en une simple API appelée par le code.
