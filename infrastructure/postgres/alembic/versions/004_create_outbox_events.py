"""Create outbox_events table

Revision ID: 004
Revises: 003
Create Date: 2026-07-30 13:50:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004"
down_revision: str | None = "003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
    create table if not exists outbox_events (
        event_id uuid primary key,
        event_type text not null,
        aggregate_type text not null,
        aggregate_id text not null,
        aggregate_version integer not null,
        tenant_id text not null,
        correlation_id uuid not null,
        causation_id uuid,
        payload jsonb not null,
        metadata jsonb not null default '{}'::jsonb,
        occurred_at timestamptz not null,
        published_at timestamptz,
        attempt_count integer not null default 0,
        next_attempt_at timestamptz,
        claimed_by text,
        claimed_at timestamptz,
        lease_until timestamptz,
        last_error text,
        status text not null default 'pending',
        constraint uq_outbox_aggregate unique (tenant_id, aggregate_type, aggregate_id, aggregate_version)
    );
    
    create index if not exists idx_outbox_status_occurred
        on outbox_events (status, occurred_at);
        
    create index if not exists idx_outbox_tenant
        on outbox_events (tenant_id);
        
    create index if not exists idx_outbox_aggregate
        on outbox_events (aggregate_type, aggregate_id);
        
    create index if not exists idx_outbox_correlation
        on outbox_events (correlation_id);
    """)


def downgrade() -> None:
    op.execute("""
    drop index if exists idx_outbox_correlation;
    drop index if exists idx_outbox_aggregate;
    drop index if exists idx_outbox_tenant;
    drop index if exists idx_outbox_status_occurred;
    drop table if exists outbox_events;
    """)
