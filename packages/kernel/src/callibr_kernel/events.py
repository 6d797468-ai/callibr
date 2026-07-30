from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from callibr_kernel.ids import new_id, new_trace_id
from callibr_kernel.time import utc_now


@dataclass(frozen=True, slots=True)
class Event:
    event_type: str
    tenant_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: new_id("evt"))
    trace_id: str = field(default_factory=new_trace_id)
    occurred_at: datetime = field(default_factory=utc_now)
    correlation_id: str | None = None
    causation_id: str | None = None


EventHandler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Event) -> int:
        handlers = [*self._handlers.get(event.event_type, []), *self._handlers.get("*", [])]
        for handler in handlers:
            handler(event)
        return len(handlers)
