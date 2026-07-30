"""Persona Engine — Declarative behaviour layer.

Prepares behaviour context (PersonaRuntime, PromptContext).
No LLM inference here.
"""

from __future__ import annotations

from typing import Any

from callibr_contracts import (
    AuditEventStore,
    PersonaDefinition,
    PersonaDefinitionStore,
    PersonaRuntime,
    PromptContext,
    ValidatePersonaResult,
)
from callibr_kernel import CallibrError, EventBus

from callibr_persona.events import PersonaEvent
from callibr_persona.registry import PersonaRegistry
from callibr_persona.runtime import build_prompt_context, build_runtime
from callibr_persona.validators import PersonaValidator


class PersonaNotFoundError(CallibrError):
    def __init__(self, persona_id: str) -> None:
        super().__init__(
            "PERSONA_NOT_FOUND",
            f"Persona {persona_id} was not found.",
            details={"persona_id": persona_id},
        )


class PersonaService:
    def __init__(
        self,
        registry: PersonaRegistry,
        validator: PersonaValidator,
        store: PersonaDefinitionStore,
        audit_event_store: AuditEventStore,
        event_bus: EventBus,
    ) -> None:
        self._registry = registry
        self._validator = validator
        self._store = store
        self._audit_event_store = audit_event_store
        self._event_bus = event_bus

    def define(self, definition: PersonaDefinition) -> PersonaDefinition:
        result = self._validator.validate(definition)
        if not result.valid:
            raise CallibrError(
                "INVALID_PERSONA",
                f"Persona validation failed: {'; '.join(result.errors)}",
                details={"errors": result.errors, "warnings": result.warnings},
            )
        self._registry.register(definition)
        self._store.save(definition)
        self._publish(
            "persona.defined",
            definition.persona_id,
            "",
            {
                "name": definition.name,
                "role": definition.role,
            },
        )
        return definition

    def get(self, persona_id: str) -> PersonaDefinition:
        definition = self._registry.get(persona_id)
        if definition is None:
            definition = self._store.get(persona_id)
            if definition is None:
                raise PersonaNotFoundError(persona_id)
            self._registry.register(definition)
        return definition

    def list(self) -> list[PersonaDefinition]:
        definitions = self._registry.list()
        if not definitions:
            definitions = self._store.list()
            for d in definitions:
                self._registry.register(d)
        return definitions

    def validate(self, persona_id: str) -> ValidatePersonaResult:
        definition = self.get(persona_id)
        result = self._validator.validate(definition)
        self._publish(
            "persona.validated",
            persona_id,
            "",
            {
                "valid": result.valid,
                "error_count": len(result.errors),
            },
        )
        return result

    def build_runtime(self, persona_id: str) -> PersonaRuntime:
        definition = self.get(persona_id)
        runtime = build_runtime(definition)
        self._publish(
            "persona.runtime_built",
            persona_id,
            "",
            {
                "runtime_id": runtime.built_at,
            },
        )
        return runtime

    def build_prompt_context(
        self,
        persona_id: str,
        crm_context: dict[str, Any] | None = None,
        scenario_context: dict[str, Any] | None = None,
        procedure_context: dict[str, Any] | None = None,
        evaluation_context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> PromptContext:
        definition = self.get(persona_id)
        runtime = build_runtime(definition)
        ctx = build_prompt_context(
            runtime,
            crm_context=crm_context,
            scenario_context=scenario_context,
            procedure_context=procedure_context,
            evaluation_context=evaluation_context,
            extra=extra,
        )
        self._publish(
            "persona.prompt_context_built",
            persona_id,
            "",
            {
                "persona_name": definition.name,
            },
        )
        return ctx

    def _publish(
        self,
        event_type: str,
        persona_id: str,
        tenant_id: str,
        payload: dict[str, Any],
    ) -> None:
        self._event_bus.publish(
            PersonaEvent(
                event_type=event_type,
                persona_id=persona_id,
                tenant_id=tenant_id,
                payload=payload,
            )
        )
