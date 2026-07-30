# ADR-0007 — Alembic pour les Migrations

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P4 — Persistence

## Contexte

Callibr utilise PostgreSQL avec SQLAlchemy. Les schemas de base de donnees evoluent avec les sprints.

Un systeme de migration est necessaire pour :

- versionner les schemas
- appliquer les changements de maniere reproductible
- permettre les rollbacks
- supporter le developpement en equipe

## Decision

Alembic est le systeme de migrations de Callibr.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| Alembic | Integration SQLAlchemy, migrations declaratives, bien documente | Necessite de comprendre les dependances |
| Django Matures | Integre a Django | Pas applicable (pas Django) |
| Migrate | Simple | Moins mature que Alembic |
| Schema manually | Controle total | Risque d'erreur, pas de versioning |

## Consequences

### Positives

- Integration native avec SQLAlchemy
- Migrations auto-generees depuis les modeles
- Historique des versions de schema
- Support du developpement en equipe

### Negatives

- Necessite de discipline sur les migrations (pas de migration manuelle)
- Les merges de migrations concurrentes peuvent etre complexes

### Neutres

- Alembic est le standard pour les projets SQLAlchemy

## References

- AEB : C03 — Enterprise Multi-Tenant SaaS Architecture
- Capability : CAP-15 — Multi-Tenant
- Implementation : Sprint 04 (Persistence & Audit Trail)
