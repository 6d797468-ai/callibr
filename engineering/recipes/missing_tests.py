"""
Recipe: Missing Tests

Quand une capability n'a pas de tests.
"""

from engineering.recipes import Recipe, RecipeStep, register_recipe

register_recipe(
    Recipe(
        id="recipe-missing-tests",
        name="Ajouter les tests pour une capability",
        description=(
            "Quand une capability n'a pas de tests, il faut creer au minimum "
            "des tests unitaires pour la logique metier et des tests"
            " d'integration pour les interfaces."
        ),
        preconditions=[
            "La capability a du code fonctionnel",
            "Aucun test n'existe pour cette capability",
        ],
        steps=[
            RecipeStep(
                order=1,
                description="Identifier les classes et fonctions critiques a tester",
                validation="Liste des classes/fonctions identifiee",
            ),
            RecipeStep(
                order=2,
                description="Creer les tests unitaires pour la logique metier",
                file_operation="create",
                file_target="tests/unit/test_<capability>.py",
                validation="Au moins 3 tests unitaires avec assertions reelles",
            ),
            RecipeStep(
                order=3,
                description="Creer les tests d'integration pour les interfaces API",
                file_operation="create",
                file_target="apps/api/tests/test_<capability>_api.py",
                validation="Les tests testent les endpoints reels",
            ),
            RecipeStep(
                order=4,
                description="Ajouter les tests au Makefile/pyproject.toml",
                validation="pytest detecte les nouveaux tests",
            ),
        ],
        validations=[
            "pytest passe pour les nouveaux tests",
            "Les tests ont des assertions reelles (pas de mocks inutiles)",
            "Les tests couvrent les cas normaux et d'erreur",
        ],
        rollback=[
            "Supprimer les fichiers de test crees",
        ],
        confidence=80.0,
    )
)
