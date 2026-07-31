import pytest
from callibr_persistence.memory.report_store import MemoryReportStore
from callibr_contracts.telemetry import ReportRecord

@pytest.fixture
def store():
    return MemoryReportStore()

def test_save_and_get_report(store):
    record = ReportRecord("s1", "<html></html>", "/path/to/report.pdf", "2026-07-31T10:00:00")
    store.save(record)
    
    saved = store.get_by_session("s1")
    assert saved is not None
    assert saved.session_id == "s1"
    assert saved.pdf_path == "/path/to/report.pdf"

def test_get_nonexistent_report(store):
    assert store.get_by_session("nonexistent") is None
