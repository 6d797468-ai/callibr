from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime

log = logging.getLogger(__name__)

PRODUCT_EVENT_TYPES = frozenset({
    "ApplicationOpened",
    "LoginSucceeded",
    "ScenarioViewed",
    "ScenarioStarted",
    "FirstMessageSent",
    "ConversationCompleted",
    "ProcedureCompleted",
    "ReportViewed",
    "ReportExported",
    "SessionResumed",
    "SessionAbandoned",
    "FeedbackSubmitted",
})


@dataclass
class ProductEvent:
    event_type: str
    tenant_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    scenario_id: str = ""
    persona_id: str = ""
    procedure_id: str = ""
    session_id: str = ""
    duration: float = 0.0
    version: str = "0.1.0"
    metadata: dict | None = None

    def __post_init__(self) -> None:
        if self.event_type not in PRODUCT_EVENT_TYPES:
            log.warning("Unknown product event type: %s", self.event_type)


class ProductEventStore:
    """In-memory store of product events.

    MVP-only: will be replaced by a persistent store when we have
    more than one pilot.
    """

    def __init__(self) -> None:
        self._events: list[ProductEvent] = []

    def record(self, event: ProductEvent) -> None:
        self._events.append(event)
        log.info(
            "PRODUCT_EVENT  type=%s  tenant=%s  scenario=%s  session=%s",
            event.event_type,
            event.tenant_id,
            event.scenario_id,
            event.session_id,
        )

    def list(self, limit: int = 200, event_type: str | None = None) -> list[ProductEvent]:
        events = self._events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]

    def count_by_type(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self._events:
            counts[e.event_type] = counts.get(e.event_type, 0) + 1
        return counts

    def clear(self) -> None:
        self._events.clear()


_SHARED_STORE: ProductEventStore | None = None


def get_product_event_store() -> ProductEventStore:
    global _SHARED_STORE
    if _SHARED_STORE is None:
        _SHARED_STORE = ProductEventStore()
    return _SHARED_STORE


def emit_product_event(
    event_type: str,
    tenant_id: str = "tenant_demo",
    scenario_id: str = "",
    persona_id: str = "",
    procedure_id: str = "",
    session_id: str = "",
    duration: float = 0.0,
    metadata: dict | None = None,
) -> None:
    store = get_product_event_store()
    event = ProductEvent(
        event_type=event_type,
        tenant_id=tenant_id,
        scenario_id=scenario_id,
        persona_id=persona_id,
        procedure_id=procedure_id,
        session_id=session_id,
        duration=duration,
        metadata=metadata,
    )
    store.record(event)
