# ADR-0001 — PostgreSQL comme SGBD Principal

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr a besoin d'un SGBD relationnel pour :

- stocker les donnees metier (tenants, users, sessions, messages, evaluations)
- garantir l'ACIDite des transactions
- supporter le multi-tenant
- scaler horizontalement en phase Enterprise

Le MVP doit etre developpe rapidement tout en preservant la capacite de passer en production.

## Decision

PostgreSQL 17 est le SGBD principal de Callibr.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| PostgreSQL | Mature, fiable, extensible, JSON support, RLS pour multi-tenant | Configuration initiale plus lourde que SQLite |
| SQLite | Zero config, parfait pour MVP | Pas de concurrence, pas de RLS, pas de scaling |
| MySQL | Populaire, bien connu | Moins riche que PostgreSQL (JSON, RLS, extensions) |
| MongoDB | Flexible, schema-less | Pas ACID, pas de relations fortes, inadapté au domaine |

## Consequences

### Positives

- Support natif du multi-tenant via Row Level Security (RLS)
- Extension pgvector pour le futur (embeddings, RAG)
- Alembic pour les migrations de schema
- Ecosystème riche (SQLAlchemy, asyncpg)
- Compatible avec la vision Enterprise de l'AEB

### Negatives

- Setup initial plus complexe que SQLite
- Necessite Docker pour le developpement local

### Neutres

- Le switch vers un autre SGBD serait possible mais coûteux

## References

- AEB : C03 — Enterprise Multi-Tenant SaaS Architecture
- Capability : CAP-15 — Multi-Tenant
- Implementation : Sprint 00 (Docker Compose avec PostgreSQL)
