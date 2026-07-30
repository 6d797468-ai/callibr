from __future__ import annotations

from typing import Annotated, Any

from callibr_api.dependencies import get_persona_service
from callibr_contracts import (
    PersonaDefinition,
    PersonaRuntime,
    PromptContext,
    ValidatePersonaResult,
)
from callibr_persona import PersonaService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/personas", tags=["Persona Engine"])


@router.get("")
def list_personas(
    service: Annotated[PersonaService, Depends(get_persona_service)],
) -> list[PersonaDefinition]:
    return service.list()


@router.post("", status_code=201)
def define_persona(
    definition: PersonaDefinition,
    service: Annotated[PersonaService, Depends(get_persona_service)],
) -> PersonaDefinition:
    return service.define(definition)


@router.get("/{persona_id}")
def get_persona(
    persona_id: str,
    service: Annotated[PersonaService, Depends(get_persona_service)],
) -> PersonaDefinition:
    return service.get(persona_id)


@router.post("/{persona_id}/validate")
def validate_persona(
    persona_id: str,
    service: Annotated[PersonaService, Depends(get_persona_service)],
) -> ValidatePersonaResult:
    return service.validate(persona_id)


@router.post("/{persona_id}/runtime")
def build_runtime(
    persona_id: str,
    service: Annotated[PersonaService, Depends(get_persona_service)],
) -> PersonaRuntime:
    return service.build_runtime(persona_id)


@router.post("/{persona_id}/prompt-context")
def build_prompt_context(
    persona_id: str,
    service: Annotated[PersonaService, Depends(get_persona_service)],
    crm_context: dict[str, Any] | None = None,
    scenario_context: dict[str, Any] | None = None,
    procedure_context: dict[str, Any] | None = None,
    evaluation_context: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> PromptContext:
    return service.build_prompt_context(
        persona_id,
        crm_context=crm_context,
        scenario_context=scenario_context,
        procedure_context=procedure_context,
        evaluation_context=evaluation_context,
        extra=extra,
    )
