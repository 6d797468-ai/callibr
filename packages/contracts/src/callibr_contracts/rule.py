from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ConditionType = Literal[
    "equals",
    "not_equals",
    "exists",
    "missing",
    "greater_than",
    "lower_than",
    "contains",
]

ActionType = Literal[
    "allow",
    "deny",
    "set_variable",
    "add_score",
    "emit_event",
    "advance_step",
    "block_transition",
]

RuleStatus = Literal["active", "inactive", "deprecated"]


class RuleReference(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    rule_version: str | None = None
    priority_override: int | None = None


class RuleCondition(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition_id: str
    type: ConditionType
    field: str
    value: Any = None
    label: str = ""


class RuleConstraint(BaseModel):
    model_config = ConfigDict(frozen=True)

    constraint_id: str
    label: str
    description: str = ""
    severity: Literal["error", "warning", "info"] = "warning"


class RuleAction(BaseModel):
    model_config = ConfigDict(frozen=True)

    action_id: str
    type: ActionType
    target: str = ""
    value: Any = None
    label: str = ""


class RuleMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    tags: list[str] = Field(default_factory=list)
    author: str = ""
    description: str = ""
    category: str = "general"


class RuleDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    version: str = "1.0.0"
    name: str
    description: str = ""
    priority: int = Field(default=100, ge=0)
    enabled: bool = True
    status: RuleStatus = "active"
    conditions: list[RuleCondition] = Field(default_factory=list)
    constraints: list[RuleConstraint] = Field(default_factory=list)
    actions: list[RuleAction] = Field(default_factory=list)
    metadata: RuleMetadata = Field(default_factory=RuleMetadata)


class ExecutionContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    variables: dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "tenant_demo"
    actor_id: str = "learner_demo"
    procedure_id: str = ""
    step_id: str = ""
    scenario_id: str = ""
    persona_id: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class RuleMatch(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    rule_name: str
    matched: bool
    priority: int
    conditions_met: list[str] = Field(default_factory=list)
    conditions_failed: list[str] = Field(default_factory=list)
    actions_applied: list[str] = Field(default_factory=list)
    score_delta: float = 0.0
    variables_set: dict[str, Any] = Field(default_factory=dict)
    events_emitted: list[str] = Field(default_factory=list)
    justification: str = ""


class RuleEvaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    results: list[RuleMatch] = Field(default_factory=list)
    matched_rules: list[str] = Field(default_factory=list)
    failed_rules: list[str] = Field(default_factory=list)
    total_score_delta: float = 0.0
    variables: dict[str, Any] = Field(default_factory=dict)
    events: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocked: bool = False


class ValidateRuleResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class RuleExplainEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    rule_name: str
    priority: int
    enabled: bool
    matched: bool
    conditions: list[dict[str, Any]] = Field(default_factory=list)
    actions: list[dict[str, Any]] = Field(default_factory=list)
    justification: str = ""


class RuleExplainResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    context: ExecutionContext
    entries: list[RuleExplainEntry] = Field(default_factory=list)
