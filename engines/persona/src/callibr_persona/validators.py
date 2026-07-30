from __future__ import annotations

from callibr_contracts import (
    PersonaDefinition,
    ValidatePersonaResult,
)

_SUPPORTED_LANGUAGES = {"fr", "en", "de", "es", "it"}
_KNOWN_TRAITS = {
    "écoute",
    "curiosité",
    "pédagogie",
    "assertivité",
    "patience",
    "adaptabilité",
    "rigueur",
    "créativité",
    "leadership",
    "collaboration",
}


class PersonaValidator:
    def validate(self, definition: PersonaDefinition) -> ValidatePersonaResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not definition.persona_id:
            errors.append("persona_id is required")
        if not definition.name:
            errors.append("name is required")

        self._validate_traits(definition, errors, warnings)
        self._validate_objectives(definition, errors, warnings)
        self._validate_constraints(definition, errors, warnings)
        self._validate_communication(definition, errors, warnings)

        return ValidatePersonaResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def _validate_traits(
        self,
        definition: PersonaDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        seen: set[str] = set()
        for trait in definition.traits:
            if not trait.trait_id:
                errors.append("each trait must have a trait_id")
                continue
            if trait.trait_id in seen:
                errors.append(f"duplicate trait_id '{trait.trait_id}'")
            seen.add(trait.trait_id)
            if trait.name not in _KNOWN_TRAITS:
                warnings.append(f"trait '{trait.trait_id}' has unknown name '{trait.name}'")

    def _validate_objectives(
        self,
        definition: PersonaDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        if not definition.objectives:
            warnings.append("no objectives defined")
            return
        seen: set[str] = set()
        for obj in definition.objectives:
            if not obj.objective_id:
                errors.append("each objective must have an objective_id")
                continue
            if obj.objective_id in seen:
                errors.append(f"duplicate objective_id '{obj.objective_id}'")
            seen.add(obj.objective_id)

    def _validate_constraints(
        self,
        definition: PersonaDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        seen: set[str] = set()
        for constraint in definition.constraints:
            if not constraint.constraint_id:
                errors.append("each constraint must have a constraint_id")
                continue
            if constraint.constraint_id in seen:
                errors.append(f"duplicate constraint_id '{constraint.constraint_id}'")
            seen.add(constraint.constraint_id)

    def _validate_communication(
        self,
        definition: PersonaDefinition,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        if definition.communication.language not in _SUPPORTED_LANGUAGES:
            errors.append(f"unsupported language '{definition.communication.language}'")
