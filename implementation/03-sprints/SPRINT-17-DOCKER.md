# Sprint 17 — Conteneurisation & Déploiement (Docker)

## Objectif

L'objectif du Sprint 17 était d'encapsuler la plateforme Callibr pour l'industrialisation finale, en s'assurant que son lancement soit autonome, idempotent et prêt pour la production via `docker-compose` ou un orchestrateur (Kubernetes).

## Statut

**Terminé.**

## Livrables

### L1 — Script d'Entrypoint (`api-entrypoint.sh`)
Création du script `infrastructure/docker/api-entrypoint.sh` pour gérer le cycle de vie du démarrage de l'API.
- Il attend de façon robuste que PostgreSQL soit prêt en se connectant au port `5432`.
- Il exécute les migrations automatiques (`alembic upgrade head`), garantissant que le schéma SQL est toujours en phase avec le code avant d'accepter du trafic, et peuplant la base de données avec le catalogue de démonstration via la logique d'Upsert (S15).
- Il passe ensuite la main à Uvicorn (`exec "$@"`).

### L2 — Optimisation du Dockerfile
Mise à jour de `infrastructure/docker/api.Dockerfile` pour copier l'arborescence complète nécessaire, incluant `infrastructure/postgres` (pour Alembic). L'image `api` définit `api-entrypoint.sh` comme son `ENTRYPOINT` principal.

### L3 — Orchestration Docker-Compose
Amélioration du `docker-compose.yml` :
- **Variables d'environnement** : Injection directe de `CALLIBR_DATABASE_URL` pointant vers le DNS interne Docker (`postgres:5432`), remplaçant la configuration locale de développement (localhost).
- **Conflits de ports** : Les ports hôtes de Redis et Postgres ont été mappés vers `16379` et `15432` pour ne pas entrer en conflit avec une instance locale (le trafic interne entre API et DB reste sur `6379` / `5432`).
- **Healthchecks** : Ajout d'une condition `service_healthy` pour s'assurer que le routage Docker attend réellement l'état `ready` de PostgreSQL avant de démarrer l'API, évitant ainsi les crashs de démarrage dus à un timeout de connexion.

### L4 — Validation des Dépendances SQLAlchemy
Correction subtile dans `env.py` : Pour que la migration s'exécute correctement via SQLAlchemy, il fallait s'assurer que le driver spécifié dans l'URL reste `postgresql+psycopg://` et ne soit pas normalisé accidentellement en `postgresql://`, ce qui forçait l'utilisation de la librairie non-installée `psycopg2`.

## Validation

- La commande `docker compose up --build -d` lance proprement les services (Redis, PostgreSQL, API, Frontend).
- L'API démarre, exécute Alembic, puis expose `http://localhost:8000/metrics`.
- Le endpoint de métriques répond en format Prometheus valide, validant le bon montage de l'API.

## Bilan
La plateforme Callibr est dorénavant 100% industrialisée : architecture découplée (S13), connectée à OpenAI avec fallback (S14), persistance asynchrone PostgreSQL (S15), instrumentée avec Prometheus (S16) et packagée sous forme de conteneurs autonomes (S17). Le projet est prêt pour le déploiement.
