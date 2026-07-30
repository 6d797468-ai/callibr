from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TenantContext:
    tenant_id: str
    user_id: str | None = None
    workspace_id: str | None = None
    trace_id: str | None = None
