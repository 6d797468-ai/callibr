# Volume E01 — AI Engineering Framework & Prompt Orchestration

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE E — AI ENGINEERING & AUTONOMOUS DEVELOPMENT
Volume E1
AI Engineering Framework & Prompt Orchestration

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

Un LLM ne doit jamais coder "au hasard".

Chaque génération doit être guidée par :

une architecture
un contexte
des contrats
des ADR
des règles
des preuves

L'IA doit raisonner comme un membre de l'équipe d'ingénierie.

2. Les rôles IA

Au lieu d'un seul prompt géant, ATOS utilise plusieurs rôles spécialisés.

Principal Architect

↓

System Architect

↓

Domain Architect

↓

Senior Backend Engineer

↓

Senior Frontend Engineer

↓

QA Engineer

↓

Security Engineer

↓

DevOps Engineer

↓

Documentation Engineer

Chaque rôle dispose d'un System Prompt spécialisé.

3. AI Orchestrator

Le moteur IA choisit automatiquement quel rôle utiliser.

User Request

↓

Task Analyzer

↓

Role Router

↓

Specialized Prompt

↓

LLM

↓

Response Validator

↓

User
4. Types de prompts

Nous distinguons plusieurs catégories.

Architecture Prompt

Définit les règles globales.

Coding Prompt

Produit du code.

Review Prompt

Analyse le code.

Refactoring Prompt

Améliore le code.

Testing Prompt

Produit les tests.

Documentation Prompt

Produit la documentation.

Audit Prompt

Contrôle la conformité.

5. Prompt Stack

Les prompts sont empilés.

Platform Prompt

↓

Architecture Prompt

↓

Project Prompt

↓

Engine Prompt

↓

Task Prompt

↓

User Prompt

Le LLM reçoit toujours un contexte hiérarchique.

6. Le Platform Prompt

Il contient.

Vision produit
Principes d'ingénierie
Contraintes
Gouvernance
ADR majeurs

Il change rarement.

7. Le Project Prompt

Il contient.

Structure du monorepo
Stack technique
Organisation
Standards Python
Règles Git
CI/CD
Conventions
8. Le Domain Prompt

Chaque Domain Pack possède son prompt.

Exemple.

Contact Center

CRM

Conversation

Training

Evaluation

Analytics

Chaque domaine possède son vocabulaire.

9. Engine Prompt

Chaque moteur possède un contexte.

Exemple.

Conversation Engine.

Le prompt contient.

Aggregate
Commands
Events
Ports
Read Models
Règles
10. Task Prompt

Le plus petit niveau.

Exemple.

Créer StartSimulationHandler

Le LLM reçoit alors uniquement le contexte utile.

11. Context Builder

Le Context Builder sélectionne.

Architecture

↓

ADR

↓

README

↓

Interfaces

↓

Tests

↓

Issue

↓

Task

Le contexte est minimal mais suffisant.

12. Prompt Registry

Tous les prompts sont versionnés.

prompts/

platform/

architecture/

engines/

tasks/

reviews/

qa/

Ils sont traités comme du code.

13. Prompt Versioning

Chaque prompt possède.

id:

owner:

version:

compatible_with:

updated_at:

Un changement de prompt est traçable.

14. Prompt Contracts

Un prompt produit toujours.

Inputs

Outputs

Constraints

Acceptance Criteria

Aucune génération libre.

15. Guardrails

Les garde-fous imposent.

Le LLM ne doit jamais :

modifier une API publique sans justification ;
casser un contrat ;
ignorer les ADR ;
supprimer des tests ;
inventer une fonctionnalité ;
modifier plusieurs domaines sans nécessité.
16. Evidence Chain

Avant de coder.

Le LLM vérifie.

Specification

↓

Architecture

↓

Contracts

↓

Existing Code

↓

Tests

↓

Implementation

Aucune hypothèse.

17. Architecture Validation

Après chaque génération.

Le code est confronté.

aux ADR ;
aux interfaces ;
aux règles d'architecture ;
aux conventions.
18. Multi-Step Generation

Les grosses tâches sont découpées.

Exemple.

Architecture

↓

Interfaces

↓

Domain

↓

Application

↓

Adapters

↓

Tests

↓

Documentation

Jamais 10 000 lignes d'un coup.

19. Review AI

Une seconde IA relit.

Elle vérifie.

architecture
qualité
sécurité
performances
lisibilité
cohérence

La génération et la revue sont séparées.

20. Self-Consistency

Pour les tâches critiques.

Le système peut générer plusieurs solutions indépendantes.

Puis comparer.

Les divergences importantes sont signalées pour revue humaine.

21. AI Knowledge Base

L'IA consulte.

ADR
Architecture Book
README
OpenAPI
Schémas
Contrats
Glossaire

Le projet constitue sa mémoire.

22. Prompt Metrics

Chaque prompt mesure.

temps
coût
taux de réussite
taux de correction
satisfaction
nombre de révisions

Les prompts sont améliorés en continu.

23. Prompt Testing

Les prompts sont testés.

Comme du logiciel.

Exemple.

Input

↓

Expected Output

↓

Evaluation

↓

Regression Tests
24. Prompt Quality

Chaque prompt doit être.

clair
déterministe autant que possible
versionné
documenté
réutilisable
modulaire
25. RAG

Les prompts n'embarquent pas tout le projet.

Ils interrogent une base documentaire.

Ordre recommandé.

ADR

↓

Architecture Book

↓

Contracts

↓

README

↓

Code

↓

Issues

Le contexte est injecté dynamiquement.

26. Prompt Security

Les prompts ne doivent jamais :

divulguer de secrets ;
ignorer les permissions ;
produire du code dangereux sans justification ;
contourner les politiques de sécurité.
27. Human-in-the-Loop

Certaines décisions restent humaines.

Exemples.

changement d'architecture ;
rupture de contrat ;
suppression d'un Engine ;
migration de données ;
évolution de sécurité.

L'IA prépare la proposition, un humain décide.

28. Prompt Lifecycle

Chaque prompt suit un cycle.

Draft

↓

Review

↓

Approved

↓

Production

↓

Deprecated

↓

Archived

Les prompts ont un propriétaire.

29. Décisions d'architecture (ADR)

Ce volume fixe les décisions suivantes :

Les prompts sont des artefacts versionnés.
Les rôles IA sont spécialisés.
Le contexte est construit dynamiquement.
Les garde-fous sont obligatoires.
Les prompts sont testés et mesurés.
Les décisions critiques restent validées par un humain.
30. Critères d'acceptation

Le Framework IA est considéré conforme lorsque :

les prompts sont organisés par rôle et version ;
le contexte est injecté automatiquement ;
les réponses respectent les ADR et les contrats ;
les revues IA sont distinctes des générations ;
les performances, les coûts et la qualité des prompts sont mesurés.
🏛️ Décision d'architecture majeure : AI as an Engineering Team

Je recommande de considérer l'IA non pas comme un unique assistant, mais comme une équipe virtuelle composée de spécialistes.

Chaque rôle possède :

ses responsabilités ;
son périmètre ;
ses critères de qualité ;
ses prompts ;
ses métriques.

Cette approche réduit les réponses monolithiques, améliore la cohérence et facilite l'évolution du système.

📘 Prochaine étape : E2 — OpenCode Development Playbook

Le prochain volume sera le manuel opérationnel d'OpenCode. Il contiendra :

le Prompt Directeur (Master Prompt) pour OpenCode ;
les règles de comportement obligatoires ;
la méthode de travail (analyse → conception → implémentation → tests → documentation) ;
les critères d'acceptation de chaque tâche ;
les workflows de développement autonomes ;
la gestion des contextes longs et des reprises de session ;
les règles de non-régression ;
la gouvernance des modifications.

Ce sera le document qui permettra à OpenCode de développer ATOS de manière progressive, cohérente et conforme à toute l'architecture définie dans les volumes précédents.
