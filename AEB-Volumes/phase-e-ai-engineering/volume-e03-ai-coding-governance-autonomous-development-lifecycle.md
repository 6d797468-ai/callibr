# Volume E03 — AI Coding Governance & Autonomous Development Lifecycle

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE E — AI ENGINEERING & AUTONOMOUS DEVELOPMENT
Volume E3
AI Coding Governance & Autonomous Development Lifecycle

Version : 1.0

Statut : Architecture de Référence

Criticité : Critique

1. Vision

OpenCode n'est pas un assistant.

OpenCode est le point d'entrée d'une équipe virtuelle composée de spécialistes.

Chaque agent possède :

une responsabilité claire ;
un périmètre limité ;
un niveau d'autorité ;
des livrables ;
des critères d'acceptation.

Aucun agent n'est autorisé à tout faire.

2. Organisation IA
                     CTO Agent

                         │

                Principal Architect

                         │

      ┌──────────────────┼─────────────────┐

      ▼                  ▼                 ▼

Domain Architect    Platform Architect   Product Architect

      ▼                  ▼                 ▼

 Backend            Frontend           Data Engineer

      ▼                  ▼                 ▼

QA Engineer      Security Engineer   DevOps Engineer

      ▼                  ▼                 ▼

 Documentation      Reviewer        Release Manager
3. Les rôles
CTO Agent

Responsable de :

vision produit ;
roadmap ;
arbitrages ;
validation des décisions majeures.

Ne code jamais.

Principal Architect

Responsable de :

architecture ;
ADR ;
interfaces ;
cohérence globale.
Domain Architect

Responsable :

moteurs métier ;
Domain Packs ;
règles métier.
Backend Engineer

Responsable :

Python ;
APIs ;
CQRS ;
Event Bus ;
moteurs.
Frontend Engineer

Responsable :

Next.js ;
UX ;
WebSocket ;
Dashboard.
QA Engineer

Produit :

tests ;
scénarios ;
couverture ;
non-régression.
Security Engineer

Contrôle :

authentification ;
RBAC ;
ABAC ;
secrets ;
OWASP.
DevOps Engineer

Responsable :

Docker ;
Kubernetes ;
GitHub Actions ;
Helm ;
Observabilité.
Documentation Engineer

Produit :

README ;
ADR ;
OpenAPI ;
diagrammes.
Reviewer

Ne produit pas de code.

Il critique.

Il valide.

Il bloque.

4. Cycle de vie d'une tâche

Une tâche suit toujours le même chemin.

Backlog

↓

Task Analysis

↓

Architecture

↓

Planning

↓

Implementation

↓

Review

↓

Testing

↓

Documentation

↓

Merge

↓

Deployment

↓

Monitoring
5. Distribution automatique

Le routeur IA décide.

Exemple.

Créer un nouvel Engine.

↓

Principal Architect

↓

Backend Engineer

↓

QA

↓

Documentation

↓

Reviewer

Correction CSS.

↓

Frontend

↓

QA

↓

Reviewer

Nouveau Provider LLM.

↓

Platform Architect

↓

Backend

↓

Security

↓

QA

↓

Reviewer

6. Autorité

Tous les agents n'ont pas le même niveau.

CTO

↓

Architect

↓

Reviewer

↓

Engineer

↓

QA

↓

Documentation

Un Backend Engineer ne peut pas modifier une ADR.

7. États d'une tâche
Draft

↓

Analysed

↓

Approved

↓

Coding

↓

Review

↓

QA

↓

Ready

↓

Merged

↓

Released

Ces états sont suivis automatiquement.

8. AI Kanban

Chaque tâche possède.

id:

title:

owner:

reviewer:

priority:

risk:

domain:

status:

Les agents lisent cet état avant toute intervention.

9. Conflits

Deux agents peuvent proposer des solutions différentes.

Le Reviewer :

compare ;
identifie les écarts ;
explique les compromis.

La décision finale peut être humaine pour les changements structurants.

10. Planning autonome

Avant de coder.

L'Architect produit.

Objectifs

Architecture

Modules

Risques

Ordre

Tests

Le code ne commence qu'après cette étape.

11. Décomposition

Une User Story devient.

Epic

↓

Feature

↓

Capability

↓

Task

↓

SubTask

Les agents travaillent sur les plus petites unités possibles.

12. Context Builder

Chaque agent reçoit uniquement son contexte.

Exemple.

QA.

↓

Tests.

↓

Contrats.

↓

Acceptance Criteria.

Backend.

↓

Interfaces.

↓

Domain.

↓

Use Cases.

↓

Handlers.

Il ne reçoit pas les maquettes Frontend.

13. Synchronisation

Tous les agents partagent.

architecture_version:

contracts_version:

prompt_version:

knowledge_version:

Ils travaillent toujours sur la même référence.

14. Gestion des conflits de code

Le Reviewer vérifie.

dépendances ;
duplication ;
dette technique ;
conventions.

Il peut refuser une modification.

15. Quality Gates IA

Avant Merge.

Le Reviewer exige.

tests ;
documentation ;
observabilité ;
conformité ADR.
16. Mémoire de travail

Chaque agent possède.

Current Task

Completed

Blocked

Dependencies

Next Action

Cette mémoire facilite les reprises de session.

17. Journal de décision

Toutes les décisions IA sont historisées.

Exemple.

decision:

reason:

alternatives:

risk:

approved_by:

Cela améliore la traçabilité.

18. Priorisation

Les agents suivent une matrice.

Priorité	Description
P0	Sécurité / Production
P1	Fonctionnalité critique
P2	Amélioration
P3	Dette technique
P4	Refactoring cosmétique
19. Gestion des blocages

Un agent peut déclarer.

Blocked

avec.

raison ;
dépendance ;
action attendue.

Aucun contournement implicite.

20. Revue croisée

Le Backend n'approuve jamais son propre code.

Le Reviewer est indépendant.

Cette séparation limite les erreurs.

21. Boucle d'amélioration

Chaque Sprint IA mesure :

taux de correction ;
taux de révision ;
temps moyen ;
coût LLM ;
défauts détectés après merge.

Ces données servent à ajuster les prompts et les processus.

22. Gouvernance documentaire

Les documents sont traités comme du code.

Architecture Book
ADR
OpenAPI
README
Diagrammes
Prompt Registry

Chaque modification est versionnée.

23. Gestion des connaissances

La base documentaire est organisée par niveaux.

Vision
    ↓
Architecture
    ↓
ADR
    ↓
Standards
    ↓
Contrats
    ↓
Code
    ↓
Tests

Les agents consultent ces niveaux dans cet ordre.

24. Escalade

Les décisions suivantes nécessitent une validation humaine :

rupture de contrat public ;
changement d'architecture ;
migration de données ;
suppression d'un Domain Pack ;
modification des politiques de sécurité ;
changement de modèle de données partagé.
25. Gestion des versions IA

Chaque agent publie :

agent:

version:

prompt_version:

knowledge_version:

compatibility:

Cela permet de reproduire un comportement à une date donnée.

26. AI Engineering Dashboard

Le tableau de bord présente :

tâches en cours ;
couverture de tests ;
conformité ADR ;
dette technique ;
coût des appels LLM ;
temps moyen de génération ;
nombre de revues ;
taux de rejet.
27. Métriques d'autonomie

L'objectif n'est pas de maximiser l'autonomie.

L'objectif est de maximiser la qualité.

Quelques indicateurs utiles :

Indicateur	Cible
Tâches sans reprise humaine	À suivre, sans objectif fixe
Régressions après fusion	Tendre vers 0
Respect des ADR	100 %
Documentation synchronisée	100 %
Tests générés et validés	≥ 90 %

Ces métriques servent à l'amélioration continue, pas à remplacer le jugement humain.

28. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Les rôles IA sont spécialisés.
Les responsabilités sont séparées.
Les décisions structurantes restent validées par un humain.
Les tâches sont atomiques.
Les revues sont indépendantes de la génération.
Les agents partagent une base de connaissances versionnée.
29. Critères d'acceptation

La gouvernance IA est considérée conforme lorsque :

chaque tâche suit un workflow défini ;
les rôles sont clairement séparés ;
les revues sont indépendantes ;
les décisions sont historisées ;
les changements majeurs sont soumis à validation.
🏛️ Décision d'architecture majeure : AI Software Factory

Je recommande que ATOS adopte officiellement une architecture de Software Factory pilotée par IA.

Cela implique que :

l'IA ne remplace pas les processus d'ingénierie ;
elle les applique de manière cohérente ;
chaque rôle IA est spécialisé et auditable ;
les décisions sont traçables ;
l'humain conserve la responsabilité des choix structurants.

Cette approche est plus robuste qu'un simple "assistant de code" et s'aligne avec les pratiques d'ingénierie logicielle modernes.

📘 Prochaine étape : E4 — RAG & Engineering Knowledge Base

Ce prochain volume décrira l'architecture de la base de connaissances d'ingénierie qui alimentera les agents IA :

découpage documentaire de l'Architecture & Engineering Book ;
indexation et versionnement ;
stratégie RAG pour le code, les ADR, les contrats et la documentation ;
recherche sémantique ;
gestion du contexte long ;
validation des sources ;
prévention des hallucinations ;
synchronisation entre la documentation et le dépôt Git.

Ce volume constituera le socle documentaire qui permettra à OpenCode et aux autres agents IA de développer ATOS en s'appuyant sur des connaissances fiables, versionnées et pertinentes.
