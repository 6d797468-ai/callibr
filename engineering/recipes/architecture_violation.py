"""
Recipe: Architecture Layer Violation

Quand un module domaine importe un module infrastructure.
"""

from engineering.recipes import Recipe, RecipeStep, register_recipe

register_recipe(
    Recipe(
        id="recipe-architecture-violation",
        name="Corriger une violation d'architecture hexagonale",
        description=(
            "Quand un module domaine importe callibr_persistence, callibr_identity "
            "ou callibr_api, il faut introduire un port (interface) pour casser le couplage."
        ),
        preconditions=[
            "Le module viole l'architecture hexagonale",
            "L'import concerne un module infrastructure",
            "Le module domaine a un besoin reel de persistance",
        ],
        steps=[
            RecipeStep(
                order=1,
                description=(
                    "Identifier le besoin : quelles operations le domaine"
                    " fait-il sur la persistance ?"
                ),
                validation="Liste des appels au module infrastructure identifiee",
            ),
            RecipeStep(
                order=2,
                description="Creer un port (interface) dans le package contracts ou kernel",
                file_operation="create",
                file_target="packages/contracts/src/callibr_contracts/ports.py",
                content='''"""
Ports — Interfaces que le domaine expose pour l'infrastructure.
"""

from typing import Protocol


class SimulationRepositoryPort(Protocol):
    """Port pour la persistance des sessions de simulation."""

    async def save(self, session: dict) -> None: ...

    async def get(self, session_id: str, tenant_id: str) -> dict | None: ...
''',
                validation="Le port est un Protocol Python",
            ),
            RecipeStep(
                order=3,
                description="Modifier le service domaine pour dependre du port, pas de l'adapter",
                file_operation="modify",
                file_target="engines/simulation/src/callibr_simulation/service.py",
                content="Remplacer 'from callibr_persistence import ...' par le port",
                validation="Plus d'import callibr_persistence dans le domaine",
            ),
            RecipeStep(
                order=4,
                description="Creer l'adapter d'infrastructure qui implemente le port",
                file_operation="create",
                file_target="packages/persistence/src/callibr_persistence/adapters.py",
                validation="L'adapter implemente le Protocol",
            ),
            RecipeStep(
                order=5,
                description="Mettre a jour les tests d'architecture",
                validation="pytest tests/architecture/ passe",
            ),
        ],
        validations=[
            "Plus d'import infrastructure dans le domaine",
            "Tests d'architecture passent",
            "Tests unitaires passent",
            "Lint propre",
        ],
        rollback=[
            "Restaurer les imports originaux",
            "Supprimer le port cree",
        ],
        confidence=85.0,
    )
)
