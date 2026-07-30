# ADR-0003 — Architecture Hexagonale

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr est une plateforme SaaS complexe qui doit :

- separer la logique metier de l'infrastructure
- permettre le remplacement de composants technique sans impacter le domaine
- faciliter les tests unitaires
- supporter l'evolution vers l'Enterprise

## Decision

Callibr adopte l'architecture hexagonale (ports & adapters) pour la structuration du code.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| Hexagonale | Separation claire domain/infrastructure, testable, evolutive | Plus de code initial, courbe d'apprentissage |
| Clean Architecture | Similaire a l'hexagonale, bien definie | Confusion possible avec Hexagonale |
| MVC traditionnel | Simple, bien connu | Couplage fort entre couches |
| Onion Architecture | Separation concentrique | Moins flexible que l'hexagonale |

## Consequences

### Positives

- Le code metier ne depend pas de FastAPI, PostgreSQL, ou tout autre framework
- Les tests unitaires peuvent tester la logique sans infrastructure
- Le remplacement de composants (ex: passer de SQLite a PostgreSQL) est isole
- Compatible avec la vision Enterprise de l'AEB

### Negatives

- Plus de code initial (ports, adapters, interfaces)
- Necessite de discipliner les-developpeurs sur la separation

### Neutres

- La structure de dossiers (engines/, platform/, packages/) reflete l'hexagonale

## References

- AEB : D01 — Monorepo, Code Organization & Engineering Standards
- AEB : D03 — Engine Implementation Blueprint
- Capability : CAP-10 — Orchestration
- Implementation : Sprint 00 (structure de dossiers)
