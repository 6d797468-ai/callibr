"""
Recipe: Missing Alembic Migrations

Quand le projet utilise PostgreSQL mais n'a pas de systeme de migrations.
"""

from engineering.recipes import Recipe, RecipeStep, register_recipe

register_recipe(
    Recipe(
        id="recipe-missing-migration",
        name="Initialiser Alembic pour les migrations PostgreSQL",
        description=(
            "Quand le projet a un schema SQL brut mais pas de systeme de migrations, "
            "il faut initialiser Alembic et creer la premiere migration depuis le schema existant."
        ),
        preconditions=[
            "Le projet utilise PostgreSQL",
            "Le dossier infrastructure/postgres/alembic/ n'existe pas",
            "Un fichier de schema SQL existe (001_runtime_state.sql)",
        ],
        steps=[
            RecipeStep(
                order=1,
                description="Initialiser Alembic",
                command="cd infrastructure/postgres && alembic init alembic",
                validation="Le dossier alembic/ est cree",
            ),
            RecipeStep(
                order=2,
                description="Configurer Alembic pour pointer vers la bonne URL de BDD",
                file_operation="modify",
                file_target="infrastructure/postgres/alembic/alembic.ini",
                validation="sqlalchemy.url pointe vers callibr",
            ),
            RecipeStep(
                order=3,
                description="Generer la premiere migration depuis le schema existant",
                command="alembic revision --autogenerate -m 'initial schema'",
                validation="Un fichier de migration est cree dans versions/",
            ),
            RecipeStep(
                order=4,
                description="Appliquer la migration",
                command="alembic upgrade head",
                validation="Les tables sont creees dans PostgreSQL",
            ),
        ],
        validations=[
            "alembic upgrade head fonctionne",
            "alembic downgrade base fonctionne",
            "Le schema correspond a 001_runtime_state.sql",
        ],
        rollback=[
            "alembic downgrade base",
            "Supprimer le dossier alembic/",
        ],
        confidence=95.0,
    )
)
