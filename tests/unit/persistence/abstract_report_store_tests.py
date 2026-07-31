import pytest
from abc import ABC, abstractmethod
from callibr_contracts.telemetry import ReportStore, ReportRecord

class AbstractReportStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> ReportStore:
        pass

    def test_save_and_get(self, store: ReportStore):
        record = ReportRecord("s1", "<html></html>", "/path/to/report.pdf", "2026-07-31T10:00:00")
        store.save(record)
        saved = store.get_by_session("s1")
        assert saved is not None
        assert saved.session_id == "s1"

    def test_get_nonexistent(self, store: ReportStore):
        assert store.get_by_session("nonexistent") is None
