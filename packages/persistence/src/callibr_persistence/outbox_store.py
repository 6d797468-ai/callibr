from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any
from uuid import UUID

from callibr_contracts import DomainEvent, OutboxRecord, OutboxStatus
from callibr_kernel.time import utc_now

from callibr_persistence.postgres import normalize_psycopg_url


class InMemoryOutboxStore:
    def __init__(self) -> None:
        self._records: dict[UUID, OutboxRecord] = {}

    def append(self, event: DomainEvent, conn: Any = None) -> None:
        if event.event_id in self._records:
            return  # Idempotent
        self._records[event.event_id] = OutboxRecord.from_event(event)

    def claim_pending(
        self, limit: int, worker_id: str, tenant_id: str | None = None
    ) -> Sequence[OutboxRecord]:
        from datetime import timedelta

        now = utc_now()
        candidates = []
        for record in self._records.values():
            if tenant_id and record.tenant_id != tenant_id:
                continue

            is_pending = record.status == OutboxStatus.PENDING and (
                record.next_attempt_at is None or record.next_attempt_at <= now
            )
            is_expired_lease = record.status == OutboxStatus.PROCESSING and (
                record.lease_until is not None and record.lease_until < now
            )

            if is_pending or is_expired_lease:
                candidates.append(record)

        candidates.sort(key=lambda r: r.occurred_at)
        batch = candidates[:limit]

        claimed = []
        for record in batch:
            updated = record.model_copy(
                update={
                    "status": OutboxStatus.PROCESSING,
                    "claimed_by": worker_id,
                    "claimed_at": now,
                    "lease_until": now + timedelta(minutes=5),
                    "attempt_count": record.attempt_count + 1,
                }
            )
            self._records[record.event_id] = updated
            claimed.append(updated)

        return claimed

    def mark_published(self, event_id: UUID, published_at: datetime) -> None:
        record = self._records.get(event_id)
        if record:
            self._records[event_id] = record.model_copy(
                update={"status": OutboxStatus.PUBLISHED, "published_at": published_at}
            )

    def mark_failed(
        self, event_id: UUID, error: str, next_attempt_at: datetime | None = None
    ) -> None:
        record = self._records.get(event_id)
        if record:
            status = OutboxStatus.PENDING if next_attempt_at else OutboxStatus.FAILED
            self._records[event_id] = record.model_copy(
                update={
                    "status": status,
                    "last_error": error,
                    "next_attempt_at": next_attempt_at,
                    "claimed_by": None,
                    "claimed_at": None,
                    "lease_until": None,
                }
            )


class PostgresOutboxStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def append(self, event: DomainEvent, conn: Any = None) -> None:
        from psycopg.types.json import Jsonb

        query = """
            insert into outbox_events (
                event_id,
                event_type,
                aggregate_type,
                aggregate_id,
                aggregate_version,
                tenant_id,
                correlation_id,
                causation_id,
                payload,
                metadata,
                occurred_at,
                status,
                attempt_count
            )
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            on conflict (event_id) do nothing;
        """
        params = (
            str(event.event_id),
            event.event_type,
            event.aggregate_type,
            event.aggregate_id,
            event.aggregate_version,
            event.tenant_id,
            str(event.correlation_id),
            str(event.causation_id) if event.causation_id else None,
            Jsonb(event.payload),
            Jsonb(event.metadata),
            event.occurred_at,
            OutboxStatus.PENDING.value,
            0,
        )

        if conn:
            conn.execute(query, params)
        else:
            from psycopg import connect

            with connect(self._database_url) as connection:
                connection.execute(query, params)

    def claim_pending(
        self, limit: int, worker_id: str, tenant_id: str | None = None
    ) -> Sequence[OutboxRecord]:
        from datetime import timedelta

        from psycopg import connect
        from psycopg.rows import dict_row

        lease_duration = timedelta(minutes=5)

        tenant_filter = "and tenant_id = %(tenant_id)s" if tenant_id else ""

        query = f"""
            with candidates as (
                select event_id
                from outbox_events
                where
                    (
                        (status = 'pending' and (next_attempt_at is null or next_attempt_at <= now()))
                        or
                        (status = 'processing' and lease_until < now())
                    )
                    {tenant_filter}
                order by occurred_at asc
                for update skip locked
                limit %(limit)s
            )
            update outbox_events as o
            set
                status = 'processing',
                claimed_by = %(worker_id)s,
                claimed_at = now(),
                lease_until = now() + %(lease)s,
                attempt_count = attempt_count + 1
            from candidates
            where o.event_id = candidates.event_id
            returning o.*;
        """

        params = {
            "limit": limit,
            "worker_id": worker_id,
            "lease": lease_duration,
        }
        if tenant_id:
            params["tenant_id"] = tenant_id

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(query, params).fetchall()

        # Parse them into OutboxRecord
        return [OutboxRecord.model_validate(row) for row in rows]

    def mark_published(self, event_id: UUID, published_at: datetime) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                update outbox_events
                set status = 'published', published_at = %s
                where event_id = %s;
                """,
                (published_at, str(event_id)),
            )

    def mark_failed(
        self, event_id: UUID, error: str, next_attempt_at: datetime | None = None
    ) -> None:
        from psycopg import connect

        status = "pending" if next_attempt_at else "failed"

        with connect(self._database_url) as connection:
            connection.execute(
                """
                update outbox_events
                set status = %s,
                    last_error = %s,
                    next_attempt_at = %s,
                    claimed_by = null,
                    claimed_at = null,
                    lease_until = null
                where event_id = %s;
                """,
                (status, error, next_attempt_at, str(event_id)),
            )
