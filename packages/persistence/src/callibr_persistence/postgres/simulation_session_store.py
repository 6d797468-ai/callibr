from __future__ import annotations

from typing import Any

from callibr_contracts import SimulationSession

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresSimulationSessionStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def save(self, session: SimulationSession) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        payload = session.model_dump(mode="json")
        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into simulation_sessions (
                    session_id, tenant_id, scenario_id, status,
                    started_at, ended_at, score, metadata
                )
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                on conflict (session_id) do update set
                    tenant_id = excluded.tenant_id,
                    scenario_id = excluded.scenario_id,
                    status = excluded.status,
                    started_at = excluded.started_at,
                    ended_at = excluded.ended_at,
                    score = excluded.score,
                    metadata = excluded.metadata,
                    updated_at = now()
                """,
                (
                    session.session_id,
                    session.tenant_id,
                    session.scenario.scenario_id,
                    session.status,
                    session.started_at,
                    session.completed_at,
                    session.evaluation.score if session.evaluation else None,
                    Jsonb(payload),
                ),
            )

    def get(self, session_id: str) -> SimulationSession | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select metadata from simulation_sessions where session_id = %s",
                (session_id,),
            ).fetchone()

        if row is None:
            return None
        return SimulationSession.model_validate(row["metadata"])

    def list(self) -> list[SimulationSession]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select metadata from simulation_sessions order by created_at desc"
            ).fetchall()
        return [SimulationSession.model_validate(r["metadata"]) for r in rows]
