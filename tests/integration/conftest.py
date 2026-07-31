import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ALEMBIC_CFG = str(REPO_ROOT / "infrastructure/postgres/alembic.ini")

skip_if_no_db = pytest.mark.skipif(
    not os.environ.get("CALLIBR_DATABASE_URL"),
    reason="CALLIBR_DATABASE_URL not set — no PostgreSQL available",
)


@pytest.fixture(scope="session")
def db_url() -> str:
    if not os.environ.get("CALLIBR_DATABASE_URL"):
        pytest.skip("CALLIBR_DATABASE_URL not set")
    from callibr_persistence.postgres import normalize_psycopg_url
    return normalize_psycopg_url(os.environ["CALLIBR_DATABASE_URL"])


@pytest.fixture(scope="session")
def migrated_db_url(db_url: str) -> str:
    os.environ["CALLIBR_DATABASE_URL"] = db_url
    from alembic.command import upgrade
    from alembic.config import Config

    cfg = Config(ALEMBIC_CFG)
    upgrade(cfg, "head")
    return db_url


@pytest.fixture(autouse=True)
def _clean_tables() -> None:
    url = os.environ.get("CALLIBR_DATABASE_URL")
    if not url:
        return
    from callibr_persistence.postgres import normalize_psycopg_url
    from psycopg import connect
    from psycopg.rows import dict_row

    with connect(normalize_psycopg_url(url), row_factory=dict_row) as connection:
        rows = connection.execute(
            "select table_name from information_schema.tables where table_schema = 'public'"
        ).fetchall()
        existing = {r["table_name"] for r in rows}
        for table in (
            "simulation_turns",
            "feedback",
            "product_events",
            "reports",
            "simulation_sessions",
            "conversation_states",
        ):
            if table in existing:
                connection.execute(f"delete from {table}")
