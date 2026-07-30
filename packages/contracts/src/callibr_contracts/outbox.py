"""Outbox contracts for durable event publishing."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from typing import Any, Protocol
from uuid import UUID, uuid4

from callibr_kernel.time import utc_now
from pydantic import BaseModel, ConfigDict, Field


class DomainEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    aggregate_type: str
    aggregate_id: str
    aggregate_version: int
    tenant_id: str
    correlation_id: UUID
    causation_id: UUID | None = None
    occurred_at: datetime = Field(default_factory=utc_now)
    payload: dict[str, object] = Field(default_factory=dict)
    metadata: dict[str, object] = Field(default_factory=dict)


class OutboxStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PUBLISHED = "published"
    FAILED = "failed"


class OutboxRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_id: UUID
    event_type: str
    aggregate_type: str
    aggregate_id: str
    aggregate_version: int
    tenant_id: str
    correlation_id: UUID
    causation_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime
    published_at: datetime | None = None
    attempt_count: int = 0
    next_attempt_at: datetime | None = None
    claimed_by: str | None = None
    claimed_at: datetime | None = None
    lease_until: datetime | None = None
    last_error: str | None = None
    status: OutboxStatus = OutboxStatus.PENDING

    @classmethod
    def from_event(cls, event: DomainEvent) -> OutboxRecord:
        return cls(
            event_id=event.event_id,
            event_type=event.event_type,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            aggregate_version=event.aggregate_version,
            tenant_id=event.tenant_id,
            correlation_id=event.correlation_id,
            causation_id=event.causation_id,
            payload=event.payload,
            metadata=event.metadata,
            occurred_at=event.occurred_at,
        )


class OutboxStore(Protocol):
    def append(self, event: DomainEvent, conn: Any = None) -> None: ...

    def claim_pending(
        self, limit: int, worker_id: str, tenant_id: str | None = None
    ) -> Sequence[OutboxRecord]: ...

    def mark_published(self, event_id: UUID, published_at: datetime) -> None: ...

    def mark_failed(
        self, event_id: UUID, error: str, next_attempt_at: datetime | None = None
    ) -> None: ...


class EventPublisher(Protocol):
    def publish(self, event: DomainEvent) -> None: ...
