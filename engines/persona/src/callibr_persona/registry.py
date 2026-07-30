from __future__ import annotations

from callibr_contracts import PersonaDefinition


class PersonaRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, PersonaDefinition] = {}

    def register(self, definition: PersonaDefinition) -> None:
        self._definitions[definition.persona_id] = definition

    def get(self, persona_id: str) -> PersonaDefinition | None:
        return self._definitions.get(persona_id)

    def list(self) -> list[PersonaDefinition]:
        return list(self._definitions.values())

    def remove(self, persona_id: str) -> None:
        self._definitions.pop(persona_id, None)
