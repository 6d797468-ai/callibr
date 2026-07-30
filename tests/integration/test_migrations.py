from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from callibr_persistence.postgres import normalize_psycopg_url
from psycopg import Connection
from psycopg.rows import dict_row

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ALEMBIC_CFG = str(REPO_ROOT / "infrastructure/postgres/alembic.ini")

EXPECTED_TABLES = {"tenants", "identity_users", "simulation_sessions", "audit_events"}

_skip_if_no_db: Any = pytest.mark.skipif(
    not __import__("os").environ.get("CALLIBR_DATABASE_URL"),
    reason="CALLIBR_DATABASE_URL not set — no PostgreSQL available",
)


def _get_test_db_url() -> str:
    url = __import__("os").environ.get("CALLIBR_DATABASE_URL", "")
    return normalize_psycopg_url(url)


def _table_exists(conn: Connection, name: str) -> bool:
    rows = conn.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
        (name,),
    ).fetchone()
    return rows[0] if rows else False


def _tables(conn: Connection) -> set[str]:
    rows = conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
    ).fetchall()
    return {r["table_name"] for r in rows}


@pytest.mark.integration
@_skip_if_no_db
def test_migration_upgrade_creates_all_tables() -> None:
    from alembic import command
    from alembic.config import Config

    url = _get_test_db_url()
    cfg = Config(ALEMBIC_CFG)
    cfg.set_main_option("sqlalchemy.url", url)

    command.downgrade(cfg, "base")

    command.upgrade(cfg, "001")

    conn = Connection.connect(url, row_factory=dict_row)
    try:
        existing = _tables(conn)
        assert EXPECTED_TABLES.issubset(existing), f"Missing tables: {EXPECTED_TABLES - existing}"
    finally:
        conn.close()


@pytest.mark.integration
@_skip_if_no_db
def test_migration_downgrade_drops_all_tables() -> None:
    from alembic import command
    from alembic.config import Config

    url = _get_test_db_url()
    cfg = Config(ALEMBIC_CFG)
    cfg.set_main_option("sqlalchemy.url", url)

    command.upgrade(cfg, "001")

    command.downgrade(cfg, "base")

    conn = Connection.connect(url, row_factory=dict_row)
    try:
        existing = _tables(conn)
        assert existing.isdisjoint(EXPECTED_TABLES), (
            f"Tables still exist after downgrade: {EXPECTED_TABLES & existing}"
        )
    finally:
        conn.close()


@pytest.mark.integration
@_skip_if_no_db
def test_migration_is_idempotent() -> None:
    from alembic import command
    from alembic.config import Config

    url = _get_test_db_url()
    cfg = Config(ALEMBIC_CFG)
    cfg.set_main_option("sqlalchemy.url", url)

    command.downgrade(cfg, "base")

    command.upgrade(cfg, "001")

    command.upgrade(cfg, "001")

    conn = Connection.connect(url, row_factory=dict_row)
    try:
        existing = _tables(conn)
        assert EXPECTED_TABLES.issubset(existing)
    finally:
        conn.close()
