import pytest
from callibr_persistence.memory.feedback_store import MemoryFeedbackStore
from callibr_contracts.telemetry import FeedbackRecord

@pytest.fixture
def store():
    return MemoryFeedbackStore()

def test_feedback_submit_and_list(store):
    record = FeedbackRecord("s1", "t1", "l1", 5, 4, 3, 4, "yes", "great", "2026-07-31T10:00:00")
    store.submit(record)
    assert len(store.list()) == 1
    assert store.list()[0] == record

def test_feedback_count_and_average(store):
    store.submit(FeedbackRecord("s1", "t1", "l1", 5, 4, 3, 4, "yes", "great", "2026-07-31T10:00:00"))
    store.submit(FeedbackRecord("s2", "t1", "l1", 3, 3, 3, 3, "no", "bad", "2026-07-31T11:00:00"))
    
    assert store.count_would_use()["yes"] == 1
    assert store.count_would_use()["no"] == 1
    assert store.average_satisfaction() == 4.0
