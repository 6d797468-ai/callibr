"""Add bridge columns to simulation_sessions: conversation_session_id, procedure_execution_id.

Revision ID: 002
Revises: 001
Create Date: 2026-07-29
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE simulation_sessions
            ADD COLUMN IF NOT EXISTS conversation_session_id TEXT,
            ADD COLUMN IF NOT EXISTS procedure_execution_id TEXT;
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS simulation_sessions_conv_session_idx
            ON simulation_sessions (conversation_session_id)
            WHERE conversation_session_id IS NOT NULL;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS simulation_sessions_conv_session_idx;
        ALTER TABLE simulation_sessions
            DROP COLUMN IF EXISTS conversation_session_id,
            DROP COLUMN IF EXISTS procedure_execution_id;
        """
    )
