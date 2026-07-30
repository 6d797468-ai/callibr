from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

StepType = Literal[
    "greeting",
    "discovery",
    "qualification",
    "solution",
    "objection",
    "closing",
    "follow_up",
    "escalation",
    "verification",
    "notification",
    "custom",
]
StepStatus = Literal["pending", "active", "completed", "failed", "skipped"]
ExecutionStatus = Literal["running", "completed", "failed", "aborted"]


class StepDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    step_id: str
    type: StepType = "custom"
    title: str
    description: str = ""
    expected_actions: list[str] = Field(default_factory=list)
    success_rules: list[str] = Field(default_factory=list)
    timeout_seconds: int | None = Field(default=None, ge=1)
    next_step: str | None = None
    order: int | None = Field(default=None, ge=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProcedureDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    procedure_id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    steps: list[StepDefinition] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def step_map(self) -> dict[str, StepDefinition]:
        return {s.step_id: s for s in self.steps}


class StepResult(BaseModel):
    step_id: str
    status: StepStatus
    started_at: datetime
    completed_at: datetime | None = None
    score: int = Field(default=0, ge=0, le=100)
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ProcedureExecution(BaseModel):
    execution_id: str
    tenant_id: str
    procedure_id: str
    procedure_version: str
    status: ExecutionStatus
    current_step_id: str | None = None
    completed_step_ids: list[str] = Field(default_factory=list)
    steps: list[StepResult] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime | None = None
    elapsed_seconds: int = Field(default=0, ge=0)
    score: int = Field(default=0, ge=0, le=100)
    context: dict[str, Any] = Field(default_factory=dict)


class StartProcedureRequest(BaseModel):
    procedure_id: str = Field(min_length=1)
    tenant_id: str = Field(default="tenant_demo", min_length=1)
    actor_id: str = Field(default="learner_demo", min_length=1)
    initial_context: dict[str, Any] = Field(default_factory=dict)


class AdvanceProcedureRequest(BaseModel):
    step_id: str = Field(min_length=1)
    output: dict[str, Any] = Field(default_factory=dict)


class ProcedureSummary(BaseModel):
    procedure_id: str
    name: str
    version: str
    description: str
    step_count: int = Field(default=0, ge=0)
