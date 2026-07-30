from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ScenarioStatus = Literal["draft", "active", "deprecated", "archived"]
ScenarioDifficulty = Literal["beginner", "intermediate", "advanced", "expert"]


class ScenarioObjective(BaseModel):
    model_config = ConfigDict(frozen=True)

    objective_id: str
    label: str
    description: str = ""
    success_criteria: list[str] = Field(default_factory=list)


class ScenarioMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    difficulty: ScenarioDifficulty = "intermediate"
    estimated_minutes: int = Field(default=15, ge=1)
    tags: list[str] = Field(default_factory=list)
    author: str = ""
    description: str = ""


class ScenarioReference(BaseModel):
    model_config = ConfigDict(frozen=True)

    procedure_id: str
    procedure_version: str | None = None
    persona_id: str
    crm_context_key: str = "default"
    rule_ids: list[str] = Field(default_factory=list)


class ScenarioDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    scenario_id: str
    version: str = "1.0.0"
    name: str
    status: ScenarioStatus = "draft"
    reference: ScenarioReference
    objectives: list[ScenarioObjective] = Field(default_factory=list)
    metadata: ScenarioMetadata = Field(default_factory=ScenarioMetadata)


class ScenarioExecutionPlan(BaseModel):
    plan_id: str
    scenario: ScenarioDefinition
    execution_context: dict[str, Any] = Field(default_factory=dict)
    composed_at: datetime
    tenant_id: str
    actor_id: str


class ScenarioExecutionResult(BaseModel):
    plan: ScenarioExecutionPlan
    execution_id: str
    status: str
    procedure_id: str


class ValidateScenarioResult(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
