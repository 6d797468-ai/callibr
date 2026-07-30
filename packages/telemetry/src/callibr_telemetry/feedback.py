from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

log = logging.getLogger(__name__)


@dataclass
class FeedbackRecord:
    session_id: str
    tenant_id: str
    learner_id: str
    satisfaction: int
    perceived_realism: int
    difficulty: int
    usefulness: int
    would_use_for_training: str
    free_text: str
    submitted_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


class FeedbackStore:
    def __init__(self) -> None:
        self._records: list[FeedbackRecord] = []

    def submit(self, record: FeedbackRecord) -> None:
        self._records.append(record)
        log.info(
            "FEEDBACK  session=%s  satisfaction=%d  would_use=%s",
            record.session_id,
            record.satisfaction,
            record.would_use_for_training,
        )

    def list(self, limit: int = 100) -> list[FeedbackRecord]:
        return self._records[-limit:]

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

    def clear(self) -> None:
        self._records.clear()


_SHARED_STORE: FeedbackStore | None = None


def get_feedback_store() -> FeedbackStore:
    global _SHARED_STORE
    if _SHARED_STORE is None:
        _SHARED_STORE = FeedbackStore()
    return _SHARED_STORE
