# Sprint 14 — Intégration LLM OpenAI

## Objectif

Connecter le `ConversationService` à un véritable modèle d'intelligence artificielle via l'API OpenAI, remplaçant ainsi le `MockAdapter` statique utilisé jusqu'à présent. Ceci permet aux Personas d'interagir dynamiquement en fonction de leur contexte et de leurs traits de personnalité.

## Statut

**Terminé.**

## Livrables

### L1 — Dépendance OpenAI
Ajout du SDK officiel `openai>=1.40.0` dans le `pyproject.toml` du projet.

### L2 — Configuration de l'API
Enrichissement de la classe `Settings` (`apps/api/src/callibr_api/config.py`) avec :
- `openai_api_key` : Clé secrète de l'API OpenAI (par défaut `None`).
- `openai_model` : Modèle utilisé pour les générations (par défaut `gpt-4o-mini` pour un ratio vitesse/coût optimal).

### L3 — `OpenAIAdapter`
Création de l'adaptateur `OpenAIAdapter` implémentant le protocole `LLMAdapter` défini dans les contrats du moteur de conversation. Cet adaptateur prend en charge :
- Le formatage des messages (System Prompt + historique).
- L'appel à l'API `chat.completions.create`.
- L'extraction de la réponse, du type d'arrêt (`finish_reason`) et de la consommation des tokens (`usage`).
- La gestion gracieuse des erreurs.

### L4 — Injection conditionnelle (Fallback)
Modification de `dependencies.py` :
- Si la clé `openai_api_key` est présente : instanciation de `OpenAIAdapter`.
- Si la clé est absente (ex: test local sans `.env`) : fallback automatique sur `MockAdapter` pour ne pas bloquer les développeurs. Un log de niveau `WARNING` est émis pour prévenir l'utilisateur.

### L5 — Suite de Tests (S14)
Ajout d'une suite de tests isolant le fonctionnement de `OpenAIAdapter` (`tests/unit/test_s14_openai_adapter.py`) en mockant la bibliothèque `openai`.

## Validation

**Couverture des Tests** : 
- 183 tests passés avec succès.
- 0 régression.

## Prochaines étapes (Sprint 15)
- Rendre les données du catalogue "Seed" persistantes via PostgreSQL pour qu'elles ne soient pas effacées en cas de redémarrage (le lifepan actuel ne les persiste pas en BDD si on redémarre).
