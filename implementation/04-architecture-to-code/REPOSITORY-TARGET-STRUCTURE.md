# Repository Target Structure

Mise a jour : 2026-07-27

## Structure Cible MVP

```text
callibr/
├── apps/
│   ├── api/
│   └── frontend/
├── packages/
│   ├── kernel/
│   ├── contracts/
│   ├── shared/
│   └── telemetry/
├── platform/
│   ├── identity/
│   ├── configuration/
│   └── observability/
├── engines/
│   ├── simulation/
│   ├── conversation/
│   ├── scenario/
│   ├── persona/
│   ├── crm/
│   ├── procedure/
│   └── evaluation/
├── domains/
│   └── support_sav/
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   └── redis/
├── deployments/
│   └── local/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── scripts/
└── pyproject.toml
```

## Regles

- `apps/` contient les points d'entree.
- `packages/` contient les librairies partagees sans metier.
- `platform/` contient les services transverses.
- `engines/` contient les moteurs produits.
- `domains/` contient les packs metier.
- `infrastructure/` contient les adaptateurs techniques.
- aucun engine ne depend directement d'un autre engine.
- les communications passent par contracts, commands, events ou services.

## Structure D'Un Engine

```text
engine/
├── domain/
├── application/
├── ports/
├── adapters/
├── infrastructure/
├── bootstrap/
└── tests/
```

## Decision MVP

Pour eviter une complexite prematuree, les premiers engines peuvent etre des packages Python dans le meme workspace.

La separation process/service viendra apres validation du MVP.

