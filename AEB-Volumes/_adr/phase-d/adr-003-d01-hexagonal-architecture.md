# ADR-003 — Hexagonal Architecture

Statut extrait : à valider

Phase : D

Volume : D01 — Monorepo, Code Organization & Engineering Standards

Source : [volume](../phase-d-engineering-standards/volume-d01-monorepo-code-organization-engineering-standards.md)

Ligne monolithe : 10557

## Décision Détectée

À compléter depuis le contexte.

## Extrait Source

```text
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
```
