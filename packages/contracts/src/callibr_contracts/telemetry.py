from typing import Protocol
from dataclasses import dataclass
from datetime import datetime

# Feedback
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
    submitted_at: str

class FeedbackStore(Protocol):
    def submit(self, record: FeedbackRecord) -> None: ...
    def list(self, limit: int = 100) -> list[FeedbackRecord]: ...
    def count_would_use(self) -> dict[str, int]: ...
    def average_satisfaction(self) -> float: ...

# Analytics
@dataclass
class ProductEvent:
    event_type: str
    tenant_id: str
    timestamp: str
    scenario_id: str
    persona_id: str
    procedure_id: str
    session_id: str
    duration: float
    version: str
    metadata: dict | None

class ProductEventStore(Protocol):
    def record(self, event: ProductEvent) -> None: ...
    def list(self, limit: int = 200, event_type: str | None = None) -> list[ProductEvent]: ...
    def count_by_type(self) -> dict[str, int]: ...

# Reports
@dataclass
class ReportRecord:
    session_id: str
    html: str
    pdf_path: str | None
    created_at: str

class ReportStore(Protocol):
    def save(self, record: ReportRecord) -> None: ...
    def get_by_session(self, session_id: str) -> ReportRecord | None: ...
