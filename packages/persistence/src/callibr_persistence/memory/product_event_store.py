from callibr_contracts.telemetry import ProductEventStore, ProductEvent

class MemoryProductEventStore:
    def __init__(self) -> None:
        self._events: list[ProductEvent] = []

    def record(self, event: ProductEvent) -> None:
        self._events.append(event)

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
