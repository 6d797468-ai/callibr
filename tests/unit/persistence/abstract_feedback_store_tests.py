from abc import ABC, abstractmethod

import pytest
from callibr_contracts.telemetry import FeedbackRecord, FeedbackStore


class AbstractFeedbackStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> FeedbackStore:
        pass

    def test_submit_and_list(self, store: FeedbackStore):
        record = FeedbackRecord("s1", "t1", "l1", 5, 4, 3, 4, "yes", "great", "2026-07-31T10:00:00")
        store.submit(record)
        assert len(store.list()) == 1

    def test_count_and_average(self, store: FeedbackStore):
        store.submit(FeedbackRecord("s1", "t1", "l1", 5, 4, 3, 4, "yes", "great", "2026-07-31T10:00:00"))
        store.submit(FeedbackRecord("s2", "t1", "l2", 3, 3, 3, 3, "no", "bad", "2026-07-31T11:00:00"))

        counts = store.count_would_use()
        assert counts["yes"] == 1
        assert counts.get("no", 0) >= 1
        assert store.average_satisfaction() == 4.0
