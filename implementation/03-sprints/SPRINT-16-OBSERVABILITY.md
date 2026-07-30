# Sprint 16 — Observabilité (Prometheus)

## Objectif

Industrialiser le monitoring de l'API Callibr en intégrant un système de métriques standardisé via `prometheus-client`. Le but est d'équiper la plateforme d'une télémétrie technique (latence, taux d'erreurs) et métier (consommation LLM, sessions de simulation) exploitable dans un environnement cloud-native.

## Statut

**Terminé.**

## Livrables

### L1 — Dépendances
Ajout de `prometheus-client>=0.20.0` dans `pyproject.toml`.

### L2 — Télémétrie (`metrics.py`)
Création du module de registre des métriques dans `packages/telemetry/src/callibr_telemetry/metrics.py` avec :
- `http_requests_total` (Counter)
- `http_request_duration_seconds` (Histogram)
- `llm_tokens_total` (Counter métier)
- `simulations_started_total` (Counter métier)

### L3 & L4 — Middleware & Endpoint
Dans `apps/api/src/callibr_api` :
- Création du `PrometheusMiddleware` pour intercepter les requêtes HTTP, chronométrer la latence et mettre à jour les compteurs avec la méthode, le path et le status code.
- Montage de l'endpoint public `GET /metrics` sur l'instance FastAPI qui expose le dump de `prometheus_client` avec le type MIME `CONTENT_TYPE_LATEST`.

### L5 & L6 — Instrumentation Métier
- **LLM Tokens** : L'adaptateur `OpenAIAdapter` incrémente dynamiquement le compteur `llm_tokens_total` (par modèle et par type : `prompt`, `completion`) avec les retours de l'API OpenAI.
- **Simulations** : Le `SimulationService` incrémente `simulations_started_total` (par `tenant_id` et `scenario_id`) à chaque nouvelle session lancée, fournissant un KPI d'usage.

### L7 — Tests
Création de `tests/api/test_s16_observability.py` pour valider que le middleware capte bien les requêtes HTTP simulées via le `TestClient` et que le dump `/metrics` contient bien les labels corrects et le format Prometheus attendu.

## Validation

- 188 tests passés avec succès.

## Prochaines étapes suggérées (Sprint 17)
- Création de la configuration Docker/Docker-compose complète pour simuler le packaging en production (API + Redis + Postgres).
