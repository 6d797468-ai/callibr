import os
import pytest
from pathlib import Path

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
    from alembic.config import Config
    from alembic.command import upgrade

    cfg = Config(ALEMBIC_CFG)
    upgrade(cfg, "head")
    return db_url
