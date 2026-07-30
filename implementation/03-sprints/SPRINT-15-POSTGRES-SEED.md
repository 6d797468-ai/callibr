# Sprint 15 — Persistance du Catalogue Seed (PostgreSQL)

## Objectif

Actuellement, les définitions des Personas, Procédures, Règles et Scénarios chargées par le composant `callibr_seed` étaient stockées en mémoire (`InMemory...Store`). L'objectif du Sprint 15 était d'implémenter la persistance de ces entités dans PostgreSQL pour une gestion durable du catalogue.

## Statut

**Terminé.**

## Livrables

### L1 — Migration Alembic 003
Création de la migration `003_seed_catalog.py` ajoutant les 5 nouvelles tables :
- `persona_definitions`
- `procedures`
- `procedure_executions`
- `rules`
- `scenario_definitions`

Chaque table utilise une clé primaire de type `TEXT` et stocke le payload complet en format `JSONB`.

### L2 à L5 — Stores PostgreSQL
Ajout des classes suivantes dans `callibr_persistence` :
- `PostgresPersonaDefinitionStore`
- `PostgresProcedureStore`
- `PostgresRuleStore`
- `PostgresScenarioDefinitionStore`

Ces classes implémentent toutes un mécanisme d'**UPSERT** (`ON CONFLICT (id) DO UPDATE SET payload = EXCLUDED.payload`), garantissant que le chargement du Seed au démarrage (lifespan de l'API) est idempotent.

### L6 — Injection des Dépendances
Mise à jour du fichier `apps/api/src/callibr_api/dependencies.py` pour instancier dynamiquement les stores Postgres si la configuration `persistence_backend` vaut `postgres`. Sinon, il retombe sur les stockages en mémoire.

### L7 — Tests d'intégration
Mise en place de tests d'intégration dans `tests/integration/test_s15_postgres_seed.py` utilisant un mock de la connexion `psycopg` pour s'assurer que les payloads générés par les modèles Pydantic (`mode="json"`) sont correctement envoyés aux commandes SQL.

## Validation

**Couverture des Tests** : 
- 187 tests passés avec succès.
- 0 régression.

## Prochaines étapes (Sprint 16)
- Ajouter l'observabilité et la métrique Prometheus.
