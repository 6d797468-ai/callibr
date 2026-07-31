from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from callibr_contracts.telemetry import FeedbackRecord, FeedbackStore

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresFeedbackStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def submit(self, record: FeedbackRecord) -> None:
        from psycopg import connect

        would = record.would_use_for_training.lower()
        if would == "yes":
            would_recommend = True
        elif would == "no":
            would_recommend = False
        else:
            would_recommend = None

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into feedback (feedback_id, session_id, tenant_id, rating, would_recommend, comment)
                values (%s, %s, %s, %s, %s, %s)
                """,
                (str(uuid4()), record.session_id, record.tenant_id,
                 record.satisfaction, would_recommend, record.free_text),
            )

    def list(self, limit: int = 100) -> list[FeedbackRecord]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select session_id, tenant_id, rating, would_recommend, comment, created_at from feedback order by created_at desc"
            ).fetchall()

        return [
            FeedbackRecord(
                session_id=r["session_id"],
                tenant_id=r["tenant_id"],
                learner_id="",
                satisfaction=r["rating"],
                perceived_realism=0,
                difficulty=0,
                usefulness=0,
                would_use_for_training="yes" if r["would_recommend"] else "no",
                free_text=r["comment"] or "",
                submitted_at=r["created_at"].isoformat(),
            )
            for r in rows[:limit]
        ]

    def count_would_use(self) -> dict[str, int]:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            rows = connection.execute(
                "select would_recommend, count(*) as cnt from feedback group by would_recommend"
            ).fetchall()

        counts: dict[str, int] = {"yes": 0, "maybe": 0, "no": 0}
        for r in rows:
            key = "yes" if r["would_recommend"] is True else ("no" if r["would_recommend"] is False else "no")
            counts[key] = r["cnt"]
        return counts

    def average_satisfaction(self) -> float:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select avg(rating) as avg_rating from feedback"
            ).fetchone()

        return float(row["avg_rating"]) if row and row["avg_rating"] else 0.0
