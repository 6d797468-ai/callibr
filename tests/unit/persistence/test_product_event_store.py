import pytest
from callibr_contracts.telemetry import ProductEvent
from callibr_persistence.memory.product_event_store import MemoryProductEventStore


@pytest.fixture
def store():
    return MemoryProductEventStore()

def test_record_and_list_events(store):
    event1 = ProductEvent("LoginSucceeded", "t1", "2026-07-31T10:00:00", "", "", "", "s1", 0.0, "0.1.0", None)
    event2 = ProductEvent("ScenarioStarted", "t1", "2026-07-31T10:05:00", "sc1", "", "", "s1", 0.0, "0.1.0", None)
    
    store.record(event1)
    store.record(event2)
    
    events = store.list()
    assert len(events) == 2
    assert events[0].event_type == "LoginSucceeded"
    assert events[1].event_type == "ScenarioStarted"

def test_count_and_filter(store):
    store.record(ProductEvent("LoginSucceeded", "t1", "2026-07-31T10:00:00", "", "", "", "s1", 0.0, "0.1.0", None))
    store.record(ProductEvent("LoginSucceeded", "t2", "2026-07-31T10:01:00", "", "", "", "s2", 0.0, "0.1.0", None))
    store.record(ProductEvent("ScenarioStarted", "t1", "2026-07-31T10:05:00", "sc1", "", "", "s1", 0.0, "0.1.0", None))
    
    assert store.count_by_type()["LoginSucceeded"] == 2
    assert len(store.list(event_type="LoginSucceeded")) == 2
