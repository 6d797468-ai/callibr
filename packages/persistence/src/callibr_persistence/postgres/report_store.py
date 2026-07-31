from __future__ import annotations

from uuid import uuid4

from callibr_contracts.telemetry import ReportRecord, ReportStore

from callibr_persistence.postgres import normalize_psycopg_url


class PostgresReportStore:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    def save(self, record: ReportRecord) -> None:
        from psycopg import connect

        with connect(self._database_url) as connection:
            connection.execute(
                """
                insert into reports (report_id, session_id, report_type, html, pdf_path)
                values (%s, %s, %s, %s, %s)
                on conflict (report_id) do nothing
                """,
                (str(uuid4()), record.session_id, "executive", record.html, record.pdf_path),
            )

    def get_by_session(self, session_id: str) -> ReportRecord | None:
        from psycopg import connect
        from psycopg.rows import dict_row

        with connect(self._database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                "select session_id, html, pdf_path, created_at from reports where session_id = %s order by created_at desc limit 1",
                (session_id,),
            ).fetchone()

        if row is None:
            return None
        return ReportRecord(
            session_id=row["session_id"],
            html=row["html"],
            pdf_path=row["pdf_path"],
            created_at=row["created_at"].isoformat(),
        )
