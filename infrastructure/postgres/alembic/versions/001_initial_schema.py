"""Create initial schema: tenants, identity_users, simulation_sessions, audit_events.

Revision ID: 001
Revises:
Create Date: 2026-07-28
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            environment TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS identity_users (
            tenant_id TEXT NOT NULL REFERENCES tenants (tenant_id),
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            display_name TEXT NOT NULL,
            roles JSONB NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            PRIMARY KEY (tenant_id, user_id)
        );
        """
    )
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS identity_users_tenant_email_idx
            ON identity_users (tenant_id, LOWER(email));
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS simulation_sessions (
            session_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            learner_id TEXT NOT NULL,
            scenario_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload JSONB NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            audit_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            tenant_id TEXT NOT NULL,
            aggregate_type TEXT NOT NULL,
            aggregate_id TEXT NOT NULL,
            occurred_at TIMESTAMPTZ NOT NULL,
            trace_id TEXT NOT NULL,
            actor_id TEXT,
            payload JSONB NOT NULL
        );
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS audit_events_aggregate_idx
            ON audit_events (aggregate_type, aggregate_id, occurred_at);
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS audit_events_tenant_idx
            ON audit_events (tenant_id, occurred_at);
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS identity_users CASCADE;")
    op.execute("DROP TABLE IF EXISTS audit_events CASCADE;")
    op.execute("DROP TABLE IF EXISTS simulation_sessions CASCADE;")
    op.execute("DROP TABLE IF EXISTS tenants CASCADE;")
