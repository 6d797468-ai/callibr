# ADR Registry

Mise a jour : 2026-07-28

## Statut

Ce registre liste tous les ADR formels du projet Callibr.

Les ADR dans `AEB-Volumes/_adr/` sont les ADR extraits de l'AEB (287 ADRs architecturaux).

Les ADR dans ce dossier `adr/` sont les ADR d'implementation (decisions prises pendant le developpement).

## ADR D'Implementation

| ID | Titre | Date | Statut |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-POSTGRESQL.md) | PostgreSQL comme SGBD Principal | 2026-07-27 | Accepte |
| [ADR-0002](ADR-0002-FASTAPI.md) | FastAPI comme Framework Backend | 2026-07-27 | Accepte |
| [ADR-0003](ADR-0003-HEXAGONAL.md) | Architecture Hexagonale | 2026-07-27 | Accepte |
| [ADR-0004](ADR-0004-MONOREPO.md) | Monorepo Modulaire | 2026-07-27 | Accepte |
| [ADR-0005](ADR-0005-VERTICAL-SLICE.md) | Vertical Slice Delivery | 2026-07-27 | Accepte |
| [ADR-0006](ADR-0006-PYDANTIC-CONTRACTS.md) | Pydantic pour les Contrats | 2026-07-27 | Accepte |
| [ADR-0007](ADR-0007-ALEMBIC-MIGRATIONS.md) | Alembic pour les Migrations | 2026-07-27 | Accepte |

## AEB Voirussi

- [Registre AEB](../AEB-Volumes/_adr/ADR-REGISTRY.md) — 287 ADRs architecturaux
- [Index AEB](../AEB-Volumes/_indexes/ADR-INDEX.md) — Index searchable

## Politique

Un ADR est requis si :

- choix technologique majeur
- changement structure repo
- contrat API public
- changement modele donnees critique
- contournement d'un principe AEB

Un ADR n'est PAS requis si :

- choix de style de code
- ajout d'un package mineur
- correction de bug
- changement de documentation
