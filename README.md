# Callibr

Callibr est une plateforme SaaS de simulation IA pour centres de contacts.
Elle permet aux agents de s'entraîner sur des mises en situation professionnelles
via un dialogue vocal ou texte avec un client virtuel, avec coaching en temps réel
et rapport exécutif.

## Parcours pilote

```text
Installation → Premier lancement → Assistant configuration
→ Choix du scénario → Simulation → Coaching temps réel
→ Rapport exécutif → Feedback → Replay
```

## Prérequis

- **Docker** 24+ avec Compose V2 (plugin)
- **Git** (pour les mises à jour)
- **Python 3.13+** (développement local uniquement)
- **Node.js 22+** (développement local uniquement)

## Installation rapide (Docker)

```bash
git clone <url-du-depot> callibr
cd callibr
cp .env.example .env
./install.sh
```

## Démarrage

```bash
./start.sh          # Lancement complet (Docker)
```

L'API est disponible sur `http://localhost:8000`.
Le frontend sur `http://localhost:5173`.

### Arrêt

```bash
./stop.sh
```

### Diagnostic

```bash
./healthcheck.sh
```

### Mise à jour

```bash
./update.sh
```

## Développement local

L'environnement virtuel et les dépendances sont gérés automatiquement :

```bash
source scripts/activate_env.sh
./dev.sh
```

Le script `dev.sh` lance le backend FastAPI (avec rechargement automatique)
et le frontend Vite simultanément. Les deux processus s'arrêtent
proprement avec `Ctrl+C`.

## Tests

```bash
python3 -m pytest          # Toute la suite
python3 -m pytest -x -q    # Rapide (arrêt au premier échec)
```

## Configuration

Copier `.env.example` vers `.env` et renseigner les variables.

Variables essentielles :

| Variable | Description | Défaut |
|---|---|---|
| `CALLIBR_AUTH_SECRET` | Clé de signature JWT (auto-générée en local) | — |
| `CALLIBR_OPENAI_API_KEY` | Clé API OpenAI (optionnel en local) | — |
| `CALLIBR_MOCK_STT` | Simulation STT | `true` |
| `CALLIBR_MOCK_TTS` | Simulation TTS | `true` |
| `CALLIBR_PERSISTENCE_BACKEND` | `memory` ou `postgres` | `memory` |

## Migrations PostgreSQL

```bash
alembic -c infrastructure/postgres/alembic.ini upgrade head
```

La base de données est automatiquement initialisée via
`infrastructure/postgres/001_runtime_state.sql` au premier démarrage Docker.

## Architecture

```text
apps/
  api/src/callibr_api/       # Backend FastAPI
  frontend/src/              # Frontend React
packages/
  contracts/                 # Contrats partagés (Pydantic)
  kernel/                    # Noyau métier
  persistence/               # Abstraction persistance
  telemetry/                 # Télémétrie, dashboard, rapports
  seed/                      # Catalogue de démonstration
platform/
  identity/                  # Authentification
engines/
  simulation/                # Moteur de simulation
  conversation/              # Runtime conversation
  evaluation/                # Évaluation des réponses
  persona/                   # Moteur de personas
  procedure/                 # Moteur de procédures
  rule/                      # Moteur de règles
  scenario/                  # Moteur de scénarios
  crm/                       # Moteur CRM
  planning/                  # Planificateur de réponses
  director/                  # Directeur de conversation
  voice/                     # Runtime vocal (STT/TTS)
```

## Sécurité

- Scan automatique des secrets au commit (pre-commit hook)
- Validation de la configuration au démarrage
- Génération automatique du secret JWT en environnement local
- Voir `ROTATION-REPORT.md` pour la gestion des clés

## Dépannage

```bash
# Vérifier l'état des services
./healthcheck.sh

# Consulter les logs
docker compose logs api
docker compose logs frontend

# Redémarrer un service
docker compose restart api

# Reconstruction complète
docker compose build --pull && docker compose up -d
```
