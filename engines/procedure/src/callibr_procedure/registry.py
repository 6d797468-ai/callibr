from __future__ import annotations

from callibr_contracts import ProcedureDefinition


class ProcedureRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, ProcedureDefinition] = {}

    def register(self, definition: ProcedureDefinition) -> None:
        self._definitions[definition.procedure_id] = definition

    def get(self, procedure_id: str) -> ProcedureDefinition | None:
        return self._definitions.get(procedure_id)

    def list(self) -> list[ProcedureDefinition]:
        return list(self._definitions.values())

    def remove(self, procedure_id: str) -> None:
        self._definitions.pop(procedure_id, None)
