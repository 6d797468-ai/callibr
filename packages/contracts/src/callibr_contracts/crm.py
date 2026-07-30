from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

CrmActionCategory = Literal["identity", "order", "ticket", "notification", "billing"]
CrmExecutionStatus = Literal["succeeded", "blocked"]


class CrmActionDefinition(BaseModel):
    action_id: str
    label: str
    category: CrmActionCategory
    description: str
    required_fields: list[str] = Field(default_factory=list)
    produces: list[str] = Field(default_factory=list)


class CrmActionExecution(BaseModel):
    execution_id: str
    action_id: str
    label: str
    status: CrmExecutionStatus
    executed_at: datetime
    message: str
    output: dict[str, Any] = Field(default_factory=dict)


class ExecuteCrmActionRequest(BaseModel):
    action_id: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class ExecuteCrmActionResponse(BaseModel):
    session_id: str
    action: CrmActionExecution
