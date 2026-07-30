from __future__ import annotations

from callibr_contracts import AuditRecord

from callibr_persistence.postgres import normalize_psycopg_url


class InMemoryAuditEventStore:
    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self._records.append(record)

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[AuditRecord]:
        return [
            record
            for record in self._records
            if record.aggregate_type == aggregate_type and record.aggregate_id == aggregate_id
        ]


class PostgresAuditEventStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def init_schema(self) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                create table if not exists audit_events (
                    audit_id text primary key,
                    event_type text not null,
                    tenant_id text not null,
                    aggregate_type text not null,
                    aggregate_id text not null,
                    occurred_at timestamptz not null,
                    trace_id text not null,
                    actor_id text,
                    payload jsonb not null
                );
                """
            )
            connection.execute(
                """
                create index if not exists audit_events_aggregate_idx
                    on audit_events (aggregate_type, aggregate_id, occurred_at);
                """
            )
            connection.execute(
                """
                create index if not exists audit_events_tenant_idx
                    on audit_events (tenant_id, occurred_at);
                """
            )

    def append(self, record: AuditRecord) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into audit_events (
                    audit_id,
                    event_type,
                    tenant_id,
                    aggregate_type,
                    aggregate_id,
                    occurred_at,
                    trace_id,
                    actor_id,
                    payload
                )
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                on conflict (audit_id) do nothing;
                """,
                (
                    record.audit_id,
                    record.event_type,
                    record.tenant_id,
                    record.aggregate_type,
                    record.aggregate_id,
                    record.occurred_at,
                    record.trace_id,
                    record.actor_id,
                    Jsonb(record.payload),
                ),
            )

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[AuditRecord]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                """
                select
                    audit_id,
                    event_type,
                    tenant_id,
                    aggregate_type,
                    aggregate_id,
                    occurred_at,
                    trace_id,
                    actor_id,
                    payload
                from audit_events
                where aggregate_type = %s and aggregate_id = %s
                order by occurred_at asc
                """,
                (aggregate_type, aggregate_id),
            ).fetchall()

        return [AuditRecord.model_validate(row) for row in rows]
