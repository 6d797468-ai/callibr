# ADR-0006 — Pydantic pour les Contrats

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr a besoin de contrats stricts entre :

- le frontend et le backend (API)
- les commands et les handlers (Command Bus)
- les events et les subscribers (Event Bus)
- les domaines entre eux

Ces contrats doivent etre valides a la compilation et au runtime.

## Decision

Pydantic est le systeme de contrats de Callibr.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| Pydantic | Validation auto, serialization, OpenAPI, bien集成 avec FastAPI | Dependance forte a Pydantic |
| Dataclasses | Natif Python, simple | Pas de validation, pas de serialization |
| attrs | Leger, flexible | Moins intégré avec FastAPI |
| Marshmallow | Mature, flexible | Moins performant, moins moderne |

## Consequences

### Positives

- Validation automatique des donnees entrees/sorties
- Serialization JSON automatique
- Documentation OpenAPI generee depuis les modeles
- Integration native avec FastAPI
- Contrats partages entre backend et frontend

### Negatives

- Dependance forte a Pydantic
- Les changements de schema necessitent des migrations

### Neutres

- Pydantic V2 est performant et stable

## References

- AEB : C01 — ATOS Kernel
- Capability : CAP-10 — Orchestration
- Implementation : Sprint 01 (contrats kernel)
