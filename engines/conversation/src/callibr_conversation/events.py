from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from callibr_kernel import utc_now


@dataclass(frozen=True)
class ConversationEvent:
    event_type: str
    session_id: str
    tenant_id: str
    occurred_at: datetime = field(default_factory=utc_now)
    payload: dict[str, Any] = field(default_factory=dict)
