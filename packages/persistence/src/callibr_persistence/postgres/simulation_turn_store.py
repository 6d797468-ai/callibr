from __future__ import annotations

from typing import Any
from uuid import uuid4

from callibr_contracts.simulation import SimulationMessage

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresSimulationTurnStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def save_turns(self, session_id: str, turns: list[SimulationMessage]) -> None:
        from psycopg import connect
        from psycopg.types.json import Jsonb

        with connect(self._database_url) as connection:
            connection.execute(
                "delete from simulation_turns where session_id = %s",
                (session_id,),
            )
            for i, msg in enumerate(turns):
                connection.execute(
                    """
                    insert into simulation_turns (turn_id, session_id, turn_number, speaker, message, evaluation)
                    values (%s, %s, %s, %s, %s, %s)
                    """,
                    (str(uuid4()), session_id, i, msg.role, msg.content, Jsonb(msg.metadata)),
                )

    def get_turns(self, session_id: str) -> list[SimulationMessage]:
        from datetime import datetime
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select turn_number, speaker, message, evaluation, created_at from simulation_turns where session_id = %s order by turn_number",
                (session_id,),
            ).fetchall()

        return [
            SimulationMessage(
                role=r["speaker"],
                content=r["message"],
                at=r["created_at"],
                metadata=r["evaluation"] or {},
            )
            for r in rows
        ]
