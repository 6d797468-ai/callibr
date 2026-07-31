from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg

from callibr_persistence.postgres import normalize_psycopg_url


class InMemoryTransactionManager:
    @contextmanager
    def transaction(self) -> Iterator[Any]:
        # Simple dummy context manager for in-memory / unit tests
        # The 'connection' yielded is just None or a dummy object
        yield None


class PostgresTransactionManager:
    def __init__(self, database_url: str) -> None:
        self._database_url = normalize_psycopg_url(database_url)

    @contextmanager
    def transaction(self) -> Iterator[psycopg.Connection]:
        with psycopg.connect(self._database_url) as conn, conn.transaction():
            # psycopg 3 manages transactions automatically.
            # Entering the block starts a transaction if none is active.
            # Normal exit will commit, exception will rollback.
            yield conn
