from __future__ import annotations

from typing import Any

import pytest
from callibr_contracts import (
    AuditRecord,
    PersonaCommunication,
    PersonaConstraint,
    PersonaDefinition,
    PersonaObjective,
    PersonaTrait,
    PromptContext,
)
from callibr_kernel import EventBus
from callibr_persona import PersonaNotFoundError, PersonaRegistry, PersonaService, PersonaValidator
from callibr_persona.runtime import build_prompt_context, build_runtime


class _InMemoryAuditStore:
    def __init__(self) -> None:
        self.records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self.records.append(record)

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[AuditRecord]:
        return [
            r
            for r in self.records
            if r.aggregate_type == aggregate_type and r.aggregate_id == aggregate_id
        ]


class _InMemoryPersonaStore:
    def __init__(self) -> None:
        self._store: dict[str, PersonaDefinition] = {}

    def save(self, definition: PersonaDefinition) -> None:
        self._store[definition.persona_id] = definition

    def get(self, persona_id: str) -> PersonaDefinition | None:
        return self._store.get(persona_id)

    def list(self) -> list[PersonaDefinition]:
        return list(self._store.values())


def _valid_persona(**overrides: Any) -> PersonaDefinition:
    kwargs: dict[str, Any] = {
        "persona_id": "senior-sales-manager",
        "name": "Senior Sales Manager",
        "description": "Commercial expérimenté B2B",
        "role": "Sales Manager",
        "tone": ["professionnel", "empathique", "structuré"],
        "traits": [
            PersonaTrait(trait_id="ecoute", name="écoute", weight=1.0),
            PersonaTrait(trait_id="curiosite", name="curiosité", weight=0.8),
        ],
        "communication": PersonaCommunication(
            style="consultatif", verbosity="medium", language="fr"
        ),
        "objectives": [
            PersonaObjective(objective_id="decouvrir", label="Découvrir les besoins"),
        ],
        "constraints": [
            PersonaConstraint(
                constraint_id="no-invent",
                label="Ne pas inventer",
                description="Ne jamais inventer de données CRM",
            ),
        ],
    }
    kwargs.update(overrides)
    return PersonaDefinition(**kwargs)


def _make_service() -> tuple[PersonaService, _InMemoryAuditStore]:
    registry = PersonaRegistry()
    validator = PersonaValidator()
    store = _InMemoryPersonaStore()
    audit_store = _InMemoryAuditStore()
    event_bus = EventBus()
    service = PersonaService(
        registry=registry,
        validator=validator,
        store=store,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )
    return service, audit_store


class TestPersonaDefinition:
    def test_define_valid_persona(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        result = service.define(persona)
        assert result.persona_id == "senior-sales-manager"
        assert result.name == "Senior Sales Manager"

    def test_define_invalid_persona_missing_id(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona(persona_id="")
        with pytest.raises(Exception, match="persona_id is required"):
            service.define(persona)

    def test_define_invalid_persona_missing_name(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona(name="")
        with pytest.raises(Exception, match="name is required"):
            service.define(persona)

    def test_define_invalid_unsupported_language(self) -> None:
        with pytest.raises(Exception, match="Input should be"):
            _valid_persona(
                communication=PersonaCommunication(
                    style="consultatif", verbosity="medium", language="zz"
                )
            )

    def test_get_persona(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        result = service.get("senior-sales-manager")
        assert result.persona_id == "senior-sales-manager"

    def test_get_missing_persona_raises(self) -> None:
        service, _ = _make_service()
        with pytest.raises(PersonaNotFoundError):
            service.get("nonexistent")

    def test_list_personas(self) -> None:
        service, _ = _make_service()
        service.define(_valid_persona(persona_id="p1", name="P1"))
        service.define(_valid_persona(persona_id="p2", name="P2"))
        results = service.list()
        assert len(results) == 2

    def test_validate_valid_persona(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        result = service.validate("senior-sales-manager")
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_persona_with_warnings(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona(objectives=[])
        service.define(persona)
        result = service.validate("senior-sales-manager")
        assert result.valid is True
        assert len(result.warnings) > 0


class TestPersonaRuntime:
    def test_build_runtime(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        runtime = service.build_runtime("senior-sales-manager")
        assert runtime.definition.persona_id == "senior-sales-manager"
        assert len(runtime.active_traits) == 2
        assert len(runtime.active_objectives) == 1
        assert len(runtime.active_constraints) == 1
        assert runtime.built_at != ""

    def test_build_runtime_missing_persona_raises(self) -> None:
        service, _ = _make_service()
        with pytest.raises(PersonaNotFoundError):
            service.build_runtime("nonexistent")


class TestPromptContext:
    def test_build_prompt_context(self) -> None:
        persona = _valid_persona()
        runtime = build_runtime(persona)
        ctx = build_prompt_context(runtime)
        assert isinstance(ctx, PromptContext)
        assert "Senior Sales Manager" in ctx.persona_prompt
        assert "Sales Manager" in ctx.system_prompt
        assert "écoute" in ctx.persona_prompt
        assert "Ne jamais inventer de données CRM" in ctx.conversation_rules

    def test_build_prompt_context_with_contexts(self) -> None:
        persona = _valid_persona()
        runtime = build_runtime(persona)
        ctx = build_prompt_context(
            runtime,
            crm_context={"company": "Acme"},
            scenario_context={"difficulty": "intermediate"},
            procedure_context={"step_id": "greeting"},
            evaluation_context={"score": 0},
            extra={"user_id": "u1"},
        )
        assert ctx.crm_context["company"] == "Acme"
        assert ctx.scenario_context["difficulty"] == "intermediate"
        assert ctx.procedure_context["step_id"] == "greeting"
        assert ctx.evaluation_context["score"] == 0
        assert ctx.extra["user_id"] == "u1"

    def test_service_build_prompt_context(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        ctx = service.build_prompt_context("senior-sales-manager")
        assert isinstance(ctx, PromptContext)
        assert "Senior Sales Manager" in ctx.persona_prompt

    def test_prompt_context_includes_constraints(self) -> None:
        persona = _valid_persona(
            constraints=[
                PersonaConstraint(
                    constraint_id="no-data",
                    label="Ne pas inventer",
                    description="Ne jamais inventer de données CRM",
                ),
                PersonaConstraint(
                    constraint_id="stay-in-scenario",
                    label="Rester dans le scénario",
                    description="Ne pas sortir du scénario en cours",
                ),
            ]
        )
        runtime = build_runtime(persona)
        ctx = build_prompt_context(runtime)
        assert "Ne jamais inventer de données CRM" in ctx.conversation_rules
        assert "Ne pas sortir du scénario en cours" in ctx.conversation_rules

    def test_prompt_context_objectives(self) -> None:
        persona = _valid_persona(
            objectives=[
                PersonaObjective(
                    objective_id="o1",
                    label="Découvrir",
                    description="Découvrir les besoins du client",
                ),
                PersonaObjective(
                    objective_id="o2",
                    label="Qualifier",
                    description="Qualifier le budget",
                ),
            ]
        )
        runtime = build_runtime(persona)
        ctx = build_prompt_context(runtime)
        assert "Découvrir" in ctx.persona_prompt
        assert "Qualifier" in ctx.persona_prompt


class TestValidator:
    def test_duplicate_trait_id(self) -> None:
        validator = PersonaValidator()
        persona = _valid_persona(
            traits=[
                PersonaTrait(trait_id="t1", name="écoute", weight=1.0),
                PersonaTrait(trait_id="t1", name="curiosité", weight=0.8),
            ]
        )
        result = validator.validate(persona)
        assert not result.valid
        assert any("duplicate trait_id" in e for e in result.errors)

    def test_duplicate_objective_id(self) -> None:
        validator = PersonaValidator()
        persona = _valid_persona(
            objectives=[
                PersonaObjective(objective_id="o1", label="Obj1"),
                PersonaObjective(objective_id="o1", label="Obj2"),
            ]
        )
        result = validator.validate(persona)
        assert not result.valid
        assert any("duplicate objective_id" in e for e in result.errors)

    def test_duplicate_constraint_id(self) -> None:
        validator = PersonaValidator()
        persona = _valid_persona(
            constraints=[
                PersonaConstraint(constraint_id="c1", label="C1"),
                PersonaConstraint(constraint_id="c1", label="C2"),
            ]
        )
        result = validator.validate(persona)
        assert not result.valid
        assert any("duplicate constraint_id" in e for e in result.errors)

    def test_unknown_trait_warning(self) -> None:
        validator = PersonaValidator()
        persona = _valid_persona(
            traits=[
                PersonaTrait.model_construct(trait_id="custom", name="unknown_trait", weight=1.0),
            ]
        )
        result = validator.validate(persona)
        assert result.valid
        assert any("unknown name" in w for w in result.warnings)

    def test_no_objectives_warning(self) -> None:
        validator = PersonaValidator()
        persona = _valid_persona(objectives=[])
        result = validator.validate(persona)
        assert result.valid
        assert any("no objectives" in w for w in result.warnings)


class TestSerialization:
    def test_persona_definition_roundtrip(self) -> None:
        persona = _valid_persona()
        serialized = persona.model_dump()
        restored = PersonaDefinition.model_validate(serialized)
        assert restored.persona_id == persona.persona_id
        assert restored.model_dump() == serialized


class TestEvents:
    def test_define_produces_event(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        result = service.define(persona)
        assert result.persona_id == "senior-sales-manager"

    def test_validate_produces_event(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        service.validate("senior-sales-manager")

    def test_build_runtime_produces_event(self) -> None:
        service, _ = _make_service()
        persona = _valid_persona()
        service.define(persona)
        service.build_runtime("senior-sales-manager")
