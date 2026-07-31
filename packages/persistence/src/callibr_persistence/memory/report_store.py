from callibr_contracts.telemetry import ReportStore, ReportRecord

class MemoryReportStore:
    def __init__(self) -> None:
        self._reports: dict[str, ReportRecord] = {}

    def save(self, record: ReportRecord) -> None:
        self._reports[record.session_id] = record

    def get_by_session(self, session_id: str) -> ReportRecord | None:
        return self._reports.get(session_id)
