from __future__ import annotations

from uuid import uuid4

from callibr_contracts.telemetry import ProductEvent, ProductEventStore

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresProductEventStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def record(self, event: ProductEvent) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into product_events (event_id, tenant_id, user_id, session_id, event_name, payload)
                values (%s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), event.tenant_id, "", event.session_id,
                 event.event_type, Jsonb(event.metadata or {})),
            )

    def list(self, limit: int = 200, event_type: str | None = None) -> list[ProductEvent]:
        from psycopg import connect
        from psycopg.rows import dict_row

        query = "select event_name, tenant_id, session_id, occurred_at from product_events"
        params: list = []
        if event_type:
            query += " where event_name = %s"
            params.append(event_type)
        query += " order by occurred_at desc"

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(query, params).fetchall()

        return [
            ProductEvent(
                event_type=r["event_name"],
                tenant_id=r["tenant_id"],
                timestamp=r["occurred_at"].isoformat(),
                session_id=r["session_id"] or "",
                scenario_id="",
                persona_id="",
                procedure_id="",
                duration=0.0,
                version="0.1.0",
                metadata=None,
            )
            for r in rows[:limit]
        ]

    def count_by_type(self) -> dict[str, int]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select event_name, count(*) as cnt from product_events group by event_name"
            ).fetchall()

        return {r["event_name"]: r["cnt"] for r in rows}
