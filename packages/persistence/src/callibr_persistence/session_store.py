from __future__ import annotations

from callibr_contracts import SimulationSession

from callibr_persistence.postgres import normalize_psycopg_url


class InMemorySimulationSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SimulationSession] = {}

    def save(self, session: SimulationSession) -> None:
        self._sessions[session.session_id] = session

    def get(self, session_id: str) -> SimulationSession | None:
        return self._sessions.get(session_id)

    def list(self) -> list[SimulationSession]:
        return list(self._sessions.values())


class PostgresSimulationSessionStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def init_schema(self) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                create table if not exists simulation_sessions (
                    session_id text primary key,
                    tenant_id text not null,
                    learner_id text not null,
                    scenario_id text not null,
                    status text not null,
                    payload jsonb not null,
                    created_at timestamptz not null default now(),
                    updated_at timestamptz not null default now()
                );
                """
            )

    def save(self, session: SimulationSession) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into simulation_sessions (
                    session_id,
                    tenant_id,
                    learner_id,
                    scenario_id,
                    status,
                    payload
                )
                values (%s, %s, %s, %s, %s, %s)
                on conflict (session_id) do update set
                    tenant_id = excluded.tenant_id,
                    learner_id = excluded.learner_id,
                    scenario_id = excluded.scenario_id,
                    status = excluded.status,
                    payload = excluded.payload,
                    updated_at = now();
                """,
                (
                    session.session_id,
                    session.tenant_id,
                    session.learner_id,
                    session.scenario.scenario_id,
                    session.status,
                    Jsonb(session.model_dump(mode="json")),
                ),
            )

    def get(self, session_id: str) -> SimulationSession | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select payload from simulation_sessions where session_id = %s",
                (session_id,),
            ).fetchone()

        if row is None:
            return None
        return SimulationSession.model_validate(row["payload"])

    def list(self) -> list[SimulationSession]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select payload from simulation_sessions order by created_at desc"
            ).fetchall()
        return [SimulationSession.model_validate(r["payload"]) for r in rows]
