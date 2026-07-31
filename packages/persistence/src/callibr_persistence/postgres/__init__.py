"""PostgreSQL persistence adapters for Callibr runtime state."""

from __future__ import annotations


def normalize_psycopg_url(database_url: str) -> str:
    if database_url.startswith("postgresql+psycopg://"):
        return database_url.replace("postgresql+psycopg://", "postgresql://", 1)
    return database_url
