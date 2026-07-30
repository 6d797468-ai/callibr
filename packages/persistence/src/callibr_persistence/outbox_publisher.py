from __future__ import annotations

import logging

from callibr_contracts import DomainEvent, EventPublisher, OutboxStore
from callibr_kernel import EventBus
from callibr_kernel.time import utc_now

logger = logging.getLogger(__name__)


class InProcessEventPublisher:
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._processed: set[str] = set()

    def publish(self, event: DomainEvent) -> None:
        # Consumer Idempotence (for in-process mock)
        event_str = str(event.event_id)
        if event_str in self._processed:
            logger.info(f"Event {event_str} already processed (idempotent skip)")
            return

        self._event_bus.publish(event)
        self._processed.add(event_str)


class OutboxPublisher:
    def __init__(
        self,
        store: OutboxStore,
        publisher: EventPublisher,
        max_retries: int = 3,
    ) -> None:
        self._store = store
        self._publisher = publisher
        self._max_retries = max_retries

    def publish_pending(
        self, limit: int = 100, worker_id: str = "worker-1", tenant_id: str | None = None
    ) -> int:
        records = self._store.claim_pending(limit=limit, worker_id=worker_id, tenant_id=tenant_id)
        if not records:
            return 0

        published_count = 0
        from datetime import timedelta

        for record in records:
            if record.attempt_count > self._max_retries:
                # Max retries exceeded, fail permanently
                self._store.mark_failed(
                    record.event_id, f"Max retries ({self._max_retries}) exceeded"
                )
                continue

            try:
                # Reconstruct DomainEvent to publish
                event = DomainEvent(
                    event_id=record.event_id,
                    event_type=record.event_type,
                    aggregate_type=record.aggregate_type,
                    aggregate_id=record.aggregate_id,
                    aggregate_version=record.aggregate_version,
                    tenant_id=record.tenant_id,
                    correlation_id=record.correlation_id,
                    causation_id=record.causation_id,
                    occurred_at=record.occurred_at,
                    payload=record.payload,
                    metadata=record.metadata,
                )

                self._publisher.publish(event)
                self._store.mark_published(record.event_id, utc_now())
                published_count += 1
            except Exception as e:
                logger.error(f"Failed to publish event {record.event_id}: {e}")
                # Backoff exponentially based on attempt_count (1, 2, 4, 8... minutes)
                backoff_mins = 2 ** (record.attempt_count - 1)
                next_attempt = utc_now() + timedelta(minutes=backoff_mins)
                self._store.mark_failed(record.event_id, str(e), next_attempt_at=next_attempt)

        return published_count
