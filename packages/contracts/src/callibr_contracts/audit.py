from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AuditRecord(BaseModel):
    audit_id: str
    event_type: str
    tenant_id: str
    aggregate_type: str
    aggregate_id: str
    occurred_at: datetime
    trace_id: str
    actor_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
