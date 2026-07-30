from __future__ import annotations

from callibr_contracts import RuleDefinition


class RuleRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, RuleDefinition] = {}

    def register(self, definition: RuleDefinition) -> None:
        self._definitions[definition.rule_id] = definition

    def get(self, rule_id: str) -> RuleDefinition | None:
        return self._definitions.get(rule_id)

    def list(self) -> list[RuleDefinition]:
        return list(self._definitions.values())

    def remove(self, rule_id: str) -> None:
        self._definitions.pop(rule_id, None)
