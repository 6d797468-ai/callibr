from __future__ import annotations

from typing import Annotated, Any

from callibr_api.dependencies import get_scenario_service
from callibr_contracts import (
    ScenarioDefinition,
    ScenarioExecutionPlan,
    ScenarioExecutionResult,
    ValidateScenarioResult,
)
from callibr_scenario import ScenarioService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/scenarios/engine", tags=["Scenario Engine"])


@router.get("")
def list_scenarios(
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
) -> list[ScenarioDefinition]:
    return service.list()


@router.post("", status_code=201)
def define_scenario(
    definition: ScenarioDefinition,
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
) -> ScenarioDefinition:
    return service.define(definition)


@router.get("/{scenario_id}")
def get_scenario(
    scenario_id: str,
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
) -> ScenarioDefinition:
    return service.get(scenario_id)


@router.post("/{scenario_id}/validate")
def validate_scenario(
    scenario_id: str,
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
) -> ValidateScenarioResult:
    return service.validate(scenario_id)


@router.post("/{scenario_id}/compose")
def compose_scenario(
    scenario_id: str,
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
    tenant_id: str = "tenant_demo",
    actor_id: str = "learner_demo",
    extra_context: dict[str, Any] | None = None,
) -> ScenarioExecutionPlan:
    return service.compose(scenario_id, tenant_id, actor_id, extra_context or {})


@router.post("/launch")
def launch_scenario(
    plan: ScenarioExecutionPlan,
    service: Annotated[ScenarioService, Depends(get_scenario_service)],
) -> ScenarioExecutionResult:
    return service.launch(plan)
