# Callibr

Callibr est une plateforme SaaS de simulation IA pour centres de contacts.

Ce workspace contient maintenant deux couches :

- l'Architecture & Engineering Book dans `AEB-Volumes/` ;
- le debut du code produit et du plan d'implementation.

## Demarrage Rapide

Backend API :

```bash
make api-dev
```

Tests :

```bash
python3 -m pytest
```

Frontend :

```bash
npm --prefix apps/frontend install
make frontend-dev
```

Runtime local complet :

```bash
docker compose up --build
```

## Documentation

- Plan d'implementation : `implementation/IMPLEMENTATION-INDEX.md`
- Etat d'implementation : `implementation/STATUS.md`
- Documentation developpeur : `docs/DEVELOPMENT.md`
- Architecture : `AEB-Volumes/AEB-MASTER-INDEX.md`

## API MVP

- `GET /health`
- `GET /api/v1/platform/info`
- `POST /api/v1/auth/login`
- `GET /api/v1/me`
- `GET /api/v1/scenarios`
- `POST /api/v1/simulations`
- `GET /api/v1/simulations/{session_id}`
- `POST /api/v1/simulations/{session_id}/messages`
- `GET /api/v1/simulations/{session_id}/crm/actions`
- `POST /api/v1/simulations/{session_id}/crm/actions`
- `GET /api/v1/simulations/{session_id}/audit`

## Persistance

Le backend demarre en memoire par defaut :

```bash
CALLIBR_PERSISTENCE_BACKEND=memory
```

Pour PostgreSQL :

```bash
CALLIBR_PERSISTENCE_BACKEND=postgres
CALLIBR_DATABASE_URL=postgresql+psycopg://callibr:callibr@postgres:5432/callibr
```

## Identifiants Demo

```text
tenant_id: tenant_demo
email: learner@demo.callibr.local
password: callibr-demo
```
