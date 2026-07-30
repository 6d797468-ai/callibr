# Volume D01 — Monorepo, Code Organization & Engineering Standards

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE D — ENGINEERING STANDARDS & IMPLEMENTATION BLUEPRINT
Volume D1
Monorepo, Code Organization & Engineering Standards

Version : 1.0

Statut : Référence d'implémentation

Criticité : Critique

1. Vision

Le projet doit rester maintenable pendant au moins 10 ans.

L'objectif n'est pas simplement d'écrire du code fonctionnel.

L'objectif est de produire une plateforme :

lisible ;
testable ;
modulaire ;
documentée ;
industrialisable ;
compréhensible par une IA.

Chaque dossier, chaque fichier et chaque classe doivent avoir une responsabilité unique.

2. Choix d'architecture

Nous retenons un Monorepo.

Pourquoi ?

Parce que :

tous les moteurs évoluent ensemble ;
les contrats doivent rester cohérents ;
les interfaces sont partagées ;
les Domain Packs dépendent du Kernel.

Un monorepo facilite :

les refactorings globaux ;
les tests d'intégration ;
la génération de documentation ;
les changements de contrats.
3. Arborescence générale
atos/

├── apps/
│   ├── api/
│   ├── gateway/
│   ├── frontend/
│   ├── admin/
│   └── cli/
│
├── kernel/
│
├── contracts/
│
├── events/
│
├── engines/
│
├── domains/
│
├── connectors/
│
├── workers/
│
├── sdk/
│
├── shared/
│
├── infrastructure/
│
├── deployment/
│
├── tools/
│
├── docs/
│
└── tests/

Chaque répertoire possède un rôle unique.

4. Les applications

Le dossier apps/ contient uniquement les points d'entrée.

Exemple.

apps/

api/

frontend/

gateway/

cli/

Aucune logique métier.

5. Kernel

Le Kernel reste extrêmement petit.

kernel/

boot/

registry/

plugin/

lifecycle/

config/

scheduler/

security/

telemetry/

Le Kernel ne connaît jamais les métiers.

6. Contracts

Les contrats sont centralisés.

contracts/

commands/

events/

services/

repositories/

dto/

responses/

Les moteurs importent les contrats.

Jamais l'inverse.

7. Events

Tous les événements vivent ici.

events/

simulation/

crm/

conversation/

analytics/

system/

security/

Les événements sont versionnés.

8. Shared

Le dossier shared/ contient uniquement.

utils/

exceptions/

types/

constants/

validators/

time/

ids/

Aucun objet métier.

9. Infrastructure

L'infrastructure technique est isolée.

postgres/

redis/

nats/

storage/

llm/

telemetry/

Le domaine n'en dépend pas directement.

10. Les Engines

Chaque moteur possède exactement la même structure.

engines/

conversation/

├── domain/
├── application/
├── ports/
├── adapters/
├── infrastructure/
├── contracts/
├── bootstrap/
└── tests/

Cette homogénéité facilite la navigation et l'automatisation.

11. Domain

Le dossier domain/ contient uniquement :

entités ;
objets valeur ;
services métier ;
agrégats ;
règles invariantes.

Aucune dépendance externe.

12. Application

Le dossier application/ contient :

cas d'usage ;
orchestrateurs ;
handlers de commandes ;
handlers de requêtes.

Le domaine est invoqué depuis cette couche.

13. Ports

Les ports définissent les interfaces.

Exemple.

ConversationRepository

LLMProvider

ScenarioRepository

EventPublisher

Aucune implémentation.

14. Adapters

Les adaptateurs implémentent les ports.

Exemple.

OpenAI Adapter

Ollama Adapter

PostgreSQL Adapter

Redis Adapter

REST Adapter

Ils peuvent être remplacés sans modifier le domaine.

15. Infrastructure interne

Le dossier infrastructure/ contient :

configuration ;
injection de dépendances ;
bootstrap ;
wiring.

Aucune logique métier.

16. Bootstrap

Chaque moteur expose un point d'entrée.

engine.bootstrap.initialize()

Le Kernel ne connaît que cette interface.

17. Tests

Chaque moteur embarque.

tests/

unit/

integration/

contract/

fixtures/

Les tests restent proches du code.

18. Convention de nommage

Classes.

SimulationEngine
ConversationRuntime
EvaluationService

Interfaces.

ISimulationEngine
ILLMProvider
IEventPublisher

Handlers.

StartSimulationHandler
CreateTicketHandler

Événements.

SimulationStarted
TicketCreated

Commandes.

StartSimulationCommand
VerifyIdentityCommand
19. Python

Nous imposons :

Python 3.13+
Typage obligatoire
from __future__ import annotations
pathlib
datetime timezone-aware
UUID
Enum
dataclass ou pydantic selon le contexte

Le code doit être compatible avec les outils d'analyse statique.

20. Style

Standards.

Ruff
Black (ou formatteur Ruff)
isort (si nécessaire)
mypy
pyright

Aucun code ne peut être fusionné sans respecter ces règles.

21. Documentation

Chaque package possède :

README.md

ADR.md

CHANGELOG.md

Les API sont documentées automatiquement.

22. ADR

Chaque décision importante possède un ADR.

Exemple.

ADR-001

Architecture Micro-Kernel
ADR-002

Event Sourcing
ADR-003

Hexagonal Architecture

Les ADR deviennent la mémoire du projet.

23. Git

Convention.

main

develop

feature/

fix/

release/

hotfix/

Les branches longues sont évitées.

24. Commits

Convention Conventional Commits.

feat:

fix:

refactor:

docs:

test:

perf:

build:

ci:

Les messages sont explicites et liés aux tickets.

25. Pull Requests

Une Pull Request doit contenir :

description ;
motivation ;
impact ;
captures (si UI) ;
ADR concerné ;
tests ajoutés ;
checklist de validation.
26. Définition de "Done"

Une fonctionnalité est terminée uniquement si :

le code compile ;
les tests passent ;
la documentation est mise à jour ;
les contrats sont versionnés ;
les métriques sont exposées ;
les logs sont présents ;
les traces sont propagées ;
les ADR sont mis à jour si nécessaire.
27. Critères de qualité

Le pipeline bloque :

couverture de tests insuffisante ;
violation des règles de typage ;
dette technique critique ;
dépendances vulnérables ;
rupture de contrat API.
28. Structure d'un Engine (Blueprint)

Tous les moteurs devront suivre ce modèle :

engine/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── aggregates/
│   ├── services/
│   └── events/
│
├── application/
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   ├── use_cases/
│   └── dto/
│
├── ports/
│
├── adapters/
│   ├── persistence/
│   ├── llm/
│   ├── messaging/
│   ├── api/
│   └── cache/
│
├── infrastructure/
├── bootstrap/
└── tests/

Cette structure est obligatoire pour tous les moteurs.

29. Décisions d'architecture (ADR)

Ce volume formalise les règles suivantes :

Monorepo unique.
Architecture hexagonale pour tous les moteurs.
Typage Python obligatoire.
Contrats partagés centralisés.
Tests au plus près du code.
Documentation versionnée.
Architecture pilotée par ADR.
Qualité contrôlée par CI.
30. Critères d'acceptation

Le référentiel sera considéré conforme lorsque :

tous les moteurs respectent la même structure ;
aucune logique métier n'est présente dans les adaptateurs ;
les dépendances pointent toujours vers le domaine (jamais l'inverse) ;
les contrats sont stables et versionnés ;
les outils de qualité sont exécutés automatiquement ;
un nouveau développeur ou un agent IA peut comprendre rapidement l'organisation du code.
🏛️ Recommandation stratégique : Boot Manifest & Architecture Manifest

Je recommande d'ajouter un composant supplémentaire qui servira de source de vérité de l'architecture.

Deux fichiers sont particulièrement utiles :

boot.yaml

Déclare les moteurs à charger, leur ordre, leurs dépendances et leurs capacités.

Exemple :

engines:
  - simulation
  - conversation
  - crm
  - evaluation
  - analytics
architecture.yaml

Décrit les versions des contrats, des événements, des Domain Packs, des API et des dépendances critiques.

Ce manifeste permet :

de vérifier automatiquement la cohérence de l'architecture ;
de détecter les incompatibilités avant le démarrage ;
d'offrir à OpenCode une vue unique et fiable de l'état de la plateforme.
Prochaine étape : D2 — Standards de Développement, Tests, Qualité et Gouvernance

Nous détaillerons :

la stratégie de tests (unitaires, intégration, contrats, E2E, performance) ;
les règles de couverture ;
la gouvernance de la dette technique ;
les standards de revue de code ;
les métriques qualité ;
la politique de versionnement des contrats ;
la gestion des migrations ;
les pratiques de sécurité (DevSecOps) ;
les exigences que chaque contribution devra satisfaire avant d'être intégrée au projet.
