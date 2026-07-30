"""Create seed catalog tables for personas, procedures, rules, and scenarios.

Revision ID: 003
Revises: 002
Create Date: 2026-07-29
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS persona_definitions (
            persona_id TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS procedures (
            procedure_id TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS procedure_executions (
            execution_id TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS rules (
            rule_id TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS scenario_definitions (
            scenario_id TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS scenario_definitions CASCADE;")
    op.execute("DROP TABLE IF EXISTS rules CASCADE;")
    op.execute("DROP TABLE IF EXISTS procedure_executions CASCADE;")
    op.execute("DROP TABLE IF EXISTS procedures CASCADE;")
    op.execute("DROP TABLE IF EXISTS persona_definitions CASCADE;")
