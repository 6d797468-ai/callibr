from __future__ import annotations

import json
from typing import Any

from callibr_contracts import ConversationState

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresConversationStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def init_schema(self) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                create table if not exists conversation_states (
                    session_id text primary key,
                    correlation_id uuid not null,
                    version integer not null,
                    payload jsonb not null,
                    created_at timestamptz not null default now(),
                    updated_at timestamptz not null default now()
                );
                """
            )

    def save(self, state: ConversationState, conn: Any = None) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        query = """
            insert into conversation_states (
                session_id, correlation_id, version, payload
            )
            values (%s, %s, %s, %s)
            on conflict (session_id) do update set
                correlation_id = excluded.correlation_id,
                version = excluded.version,
                payload = excluded.payload,
                updated_at = now()
        """
        params = (
            state.session_id,
            state.correlation_id,
            state.version,
            Jsonb(json.loads(state.model_dump_json())),
        )

        if conn:
            conn.execute(query, params)
        else:
            with connect(self._database_url) as connection:
                connection.execute(query, params)

    def get(self, session_id: str) -> ConversationState | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select payload from conversation_states where session_id = %s",
                (session_id,),
            ).fetchone()

        if row is None:
            return None
        return ConversationState.model_validate(row["payload"])
