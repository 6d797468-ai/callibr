from callibr_contracts.telemetry import FeedbackRecord


class MemoryFeedbackStore:
    def __init__(self) -> None:
        self._records: list[FeedbackRecord] = []

    def submit(self, record: FeedbackRecord) -> None:
        self._records.append(record)

    def list(self, limit: int = 100) -> list[FeedbackRecord]:
        return self._records[-limit:]

    def count(self) -> int:
        return len(self._records)

    def count_would_use(self) -> dict[str, int]:
        counts: dict[str, int] = {"yes": 0, "maybe": 0, "no": 0}
        for r in self._records:
            if r.would_use_for_training in counts:
                counts[r.would_use_for_training] += 1
        return counts

    def average_satisfaction(self) -> float:
        if not self._records:
            return 0.0
        return sum(r.satisfaction for r in self._records) / len(self._records)
