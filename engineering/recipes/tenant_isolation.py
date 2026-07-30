"""
Recipe: Tenant Isolation

Quand un store ou repository ne filtre pas par tenant_id.
"""

from engineering.recipes import Recipe, RecipeStep, register_recipe

register_recipe(
    Recipe(
        id="recipe-tenant-isolation",
        name="Ajouter l'isolation de tenant a un store",
        description=(
            "Quand un store ne contient pas tenant_id, il faut ajouter le filtrage "
            "par tenant pour garantir l'isolation des donnees multi-tenant."
        ),
        preconditions=[
            "Le store n'a pas de reference a tenant_id",
            "Le store n'est pas un fichier de test",
            "Le store est utilise dans un contexte multi-tenant",
        ],
        steps=[
            RecipeStep(
                order=1,
                description="Identifier les methodes du store qui accedent aux donnees",
                validation="Liste des methodes identifiee",
            ),
            RecipeStep(
                order=2,
                description="Ajouter le parametre tenant_id a chaque methode publique",
                validation="Chaque methode a un parametre tenant_id: str",
            ),
            RecipeStep(
                order=3,
                description="Ajouter le filtrage WHERE tenant_id dans les requetes SQL",
                validation="Chaque requete SQL contient WHERE tenant_id = :tenant_id",
            ),
            RecipeStep(
                order=4,
                description="Mettre a jour les appels du service pour passer le tenant_id",
                validation="Les services passent tenant_id du TenantContext",
            ),
            RecipeStep(
                order=5,
                description="Ajouter un test d'isolation cross-tenant",
                validation="Le test verifie qu'un tenant ne peut pas lire les donnees d'un autre",
            ),
        ],
        validations=[
            "Chaque methode du store a un parametre tenant_id",
            "Les requetes SQL filtrent par tenant_id",
            "Test d'isolation cross-tenant passe",
            "Tests existants passent",
        ],
        rollback=[
            "Supprimer les parametres tenant_id ajoutes",
            "Restaurer les requetes SQL originales",
        ],
        confidence=90.0,
    )
)
