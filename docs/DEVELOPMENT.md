# Development

Mise a jour : 2026-07-27

## Objectif

Ce document explique comment demarrer le bootstrap local Callibr.

## Backend

Commande recommandee apres installation des dependances :

```bash
make api-dev
```

Healthcheck :

```bash
curl http://localhost:8000/health
```

Utilisateur courant :

```bash
curl -H "X-Tenant-Id: tenant_demo" -H "X-User-Id: learner_demo" http://localhost:8000/api/v1/me
```

Login local :

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"tenant_demo","email":"learner@demo.callibr.local","password":"callibr-demo"}'
```

## Frontend

Depuis `apps/frontend` :

```bash
npm --prefix apps/frontend install
make frontend-dev
```

## Docker Compose

```bash
docker compose up --build
```

Le schema PostgreSQL initial se trouve dans `infrastructure/postgres/001_runtime_state.sql`.

Pour activer les stores PostgreSQL dans l'API :

```bash
CALLIBR_PERSISTENCE_BACKEND=postgres
```

## Tests Backend

```bash
python3 -m pytest
```

## Sprint Courant

P1 — Simulation Core MVP.

Voir :

`implementation/STATUS.md`

## Verification

```bash
make lint
python3 -m pytest
npm --prefix apps/frontend run build
```
