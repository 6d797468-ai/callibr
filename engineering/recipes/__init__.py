"""
Callibr Recipes — Reusable Problem-Solving Patterns

Chaque recette decrit comment resoudre une famille de problemes.
Elle contient : preconditions, etapes, validations, rollback.
"""

from dataclasses import dataclass


@dataclass
class RecipeStep:
    order: int
    description: str
    command: str | None = None
    file_operation: str | None = None  # "create", "modify", "delete"
    file_target: str | None = None
    content: str | None = None
    validation: str | None = None


@dataclass
class Recipe:
    id: str
    name: str
    description: str
    preconditions: list[str]
    steps: list[RecipeStep]
    validations: list[str]
    rollback: list[str]
    confidence: float  # 0-100


RECIPES: dict[str, Recipe] = {}


def register_recipe(recipe: Recipe):
    RECIPES[recipe.id] = recipe


def get_recipe(recipe_id: str) -> Recipe | None:
    return RECIPES.get(recipe_id)


def find_recipes_for_diagnostic(check_id: str) -> list[Recipe]:
    matches = []
    for recipe in RECIPES.values():
        if check_id in recipe.id or check_id.replace("chk-", "") in recipe.id:
            matches.append(recipe)
    return matches
