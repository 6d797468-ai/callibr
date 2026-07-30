# ADR-0002 — FastAPI comme Framework Backend

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr a besoin d'un framework backend Python pour :

- exposer une API REST
- supporter l'asynchronisme (async/await)
- generer automatiquement la documentation OpenAPI
- etre performant pour le MVP et au-dela

## Decision

FastAPI est le framework backend principal de Callibr.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| FastAPI | Async natif, auto-doc OpenAPI, Pydantic intégré, performant | Communauté plus petite que Django/Flask |
| Django | Batteries-inclues, admin, ORM mature | Sync par defaut, plus lourd, moins moderne |
| Flask | Simple, flexible, legere | Pas d'async natif, pas d'auto-doc |
| Litestar | Alternatives moderne à FastAPI | Communauté encore plus petite |

## Consequences

### Positives

- Integration native avec Pydantic (contrats)
- Documentation OpenAPI automatique
- Async/await natif pour les appels LLM futurs
- Performance comparable à Node.js/Go pour les API REST
- Compatible avec la vision monorepo de l'AEB

### Negatives

- Moins de "batteries-inclues" que Django (pas d'admin, pas d'ORM integre)
- Necessite de choisir ses propres outils (SQLAlchemy, Alembic, etc.)

### Neutres

- Le switch vers un autre framework serait possible mais coûteux

## References

- AEB : C01 — ATOS Kernel
- AEB : C04 — API Gateway, Integration Platform & SDK
- Capability : CAP-10 — Orchestration
- Implementation : Sprint 00 (FastAPI shell)
