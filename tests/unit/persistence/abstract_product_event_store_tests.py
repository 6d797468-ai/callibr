from abc import ABC, abstractmethod

import pytest
from callibr_contracts.telemetry import ProductEvent, ProductEventStore


class AbstractProductEventStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> ProductEventStore:
        pass

    def test_record_and_list(self, store: ProductEventStore):
        store.record(ProductEvent("LoginSucceeded", "t1", "2026-07-31T10:00:00", "", "", "", "s1", 0.0, "0.1.0", None))
        store.record(ProductEvent("ScenarioStarted", "t1", "2026-07-31T10:05:00", "sc1", "", "", "s1", 0.0, "0.1.0", None))

        events = store.list()
        assert len(events) == 2

    def test_filter_and_count(self, store: ProductEventStore):
        store.record(ProductEvent("LoginSucceeded", "t1", "2026-07-31T10:00:00", "", "", "", "s1", 0.0, "0.1.0", None))
        store.record(ProductEvent("LoginSucceeded", "t2", "2026-07-31T10:01:00", "", "", "", "s2", 0.0, "0.1.0", None))
        store.record(ProductEvent("ScenarioStarted", "t1", "2026-07-31T10:05:00", "sc1", "", "", "s1", 0.0, "0.1.0", None))

        assert store.count_by_type()["LoginSucceeded"] == 2
        assert len(store.list(event_type="LoginSucceeded")) == 2
