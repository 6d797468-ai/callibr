"""
Callibr Execution Plan Generator

Transforme un diagnostic en plan d'action executable.
"""

from dataclasses import dataclass

from engineering.diagnostics import Diagnostic
from engineering.recipes import find_recipes_for_diagnostic


@dataclass
class ExecutionStep:
    order: int
    description: str
    confidence: float
    command: str | None = None
    file_target: str | None = None
    validation: str | None = None
    auto_executable: bool = False


@dataclass
class ExecutionPlan:
    diagnostic: Diagnostic
    recipe_name: str | None
    steps: list[ExecutionStep]
    overall_confidence: float
    auto_executable: bool  # True si toutes les etapes sont >= 95%

    def summary(self) -> str:
        lines = []
        lines.append(f"EXECUTION PLAN — {self.diagnostic.title}")
        lines.append(f"Confiance globale : {self.overall_confidence:.0f}%")
        lines.append(f"Auto-executable : {'OUI' if self.auto_executable else 'NON'}")
        lines.append("")
        if self.recipe_name:
            lines.append(f"Recette : {self.recipe_name}")
            lines.append("")
        for step in self.steps:
            auto = "AUTO" if step.auto_executable else "MANUEL"
            lines.append(f"  Etape {step.order} [{auto}] [{step.confidence:.0f}%]")
            lines.append(f"    {step.description}")
            if step.command:
                lines.append(f"    Commande : {step.command}")
            if step.file_target:
                lines.append(f"    Fichier  : {step.file_target}")
            if step.validation:
                lines.append(f"    Validation : {step.validation}")
            lines.append("")
        return "\n".join(lines)


def generate_execution_plan(diagnostic: Diagnostic) -> ExecutionPlan:
    recipes = find_recipes_for_diagnostic(diagnostic.check_id)

    if recipes:
        recipe = recipes[0]
        steps = []
        for recipe_step in recipe.steps:
            confidence = recipe.confidence
            auto = confidence >= 95.0 and recipe_step.command is not None
            steps.append(
                ExecutionStep(
                    order=recipe_step.order,
                    description=recipe_step.description,
                    confidence=confidence,
                    command=recipe_step.command,
                    file_target=recipe_step.file_target,
                    validation=recipe_step.validation,
                    auto_executable=auto,
                )
            )

        overall = recipe.confidence
        auto_all = all(s.auto_executable for s in steps)

        return ExecutionPlan(
            diagnostic=diagnostic,
            recipe_name=recipe.name,
            steps=steps,
            overall_confidence=overall,
            auto_executable=auto_all,
        )

    steps = [
        ExecutionStep(
            order=1,
            description=f"Analyser le probleme : {diagnostic.title}",
            confidence=100.0,
            auto_executable=True,
        ),
        ExecutionStep(
            order=2,
            description=f"Appliquer le fix : {diagnostic.fix_proposal[:100]}",
            confidence=50.0,
            auto_executable=False,
            validation="Verifier que le probleme est resolu",
        ),
        ExecutionStep(
            order=3,
            description="Executer les tests pour valider",
            confidence=80.0,
            command="pytest",
            auto_executable=True,
        ),
    ]

    avg_confidence = sum(s.confidence for s in steps) / len(steps)

    return ExecutionPlan(
        diagnostic=diagnostic,
        recipe_name=None,
        steps=steps,
        overall_confidence=avg_confidence,
        auto_executable=False,
    )


def generate_all_plans() -> list[ExecutionPlan]:
    from engineering.diagnostics import run_all_diagnostics

    diagnostics = run_all_diagnostics()
    plans = []
    for d in diagnostics:
        if not d.passed:
            plans.append(generate_execution_plan(d))
    return plans
