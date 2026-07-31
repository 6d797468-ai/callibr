"""Extend simulation_sessions and create pilot persistence tables

Revision ID: 005
Revises: 004
Create Date: 2026-07-31 10:00:00.000000

Note: the pilot persistence schema is applied in place on the legacy
simulation_sessions table (created by 001), because the legacy
PostgresSimulationSessionStore and the pilot stores share the same table.
session_id / status / speaker stay TEXT to match the frozen contracts
(SimulationSession.session_id is a free string and SimulationStatus is
Literal["active", "completed"]). No FK from turns/feedback/reports to
simulation_sessions: the MemoryStores accept orphan rows, and Postgres
must behave identically.
"""

from collections.abc import Sequence
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "005"
down_revision: str | None = "004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.execute("""
    -- 1. Extend the legacy simulation_sessions (created in 001) with the
    --    structured pilot persistence columns (all nullable so the legacy
    --    store keeps working untouched).
    alter table simulation_sessions
        add column if not exists persona_id text,
        add column if not exists procedure_id text,
        add column if not exists started_at timestamptz,
        add column if not exists ended_at timestamptz,
        add column if not exists duration_ms bigint,
        add column if not exists score numeric(5,2),
        add column if not exists readiness_score numeric(5,2),
        add column if not exists metadata jsonb;

    -- 2. The pilot store writes structured rows and does not populate the
    --    legacy learner_id / payload columns.
    alter table simulation_sessions
        alter column learner_id drop not null,
        alter column payload drop not null;

    create index if not exists idx_sessions_tenant_started on simulation_sessions(tenant_id, started_at);
    create index if not exists idx_sessions_scenario on simulation_sessions(scenario_id);
    create index if not exists idx_sessions_status on simulation_sessions(status);

    -- 3. simulation_turns
    create table if not exists simulation_turns (
        turn_id uuid primary key,
        session_id text not null,
        turn_number integer not null,
        speaker text not null,
        message text not null,
        evaluation jsonb,
        created_at timestamptz not null default now(),
        unique(session_id, turn_number)
    );
    create index if not exists idx_turns_session_number on simulation_turns(session_id, turn_number);

    -- 4. feedback
    create table if not exists feedback (
        feedback_id uuid primary key,
        session_id text not null,
        tenant_id text not null,
        rating integer not null check (rating between 1 and 5),
        would_recommend boolean,
        comment text,
        created_at timestamptz not null default now()
    );
    create index if not exists idx_feedback_tenant on feedback(tenant_id);
    create index if not exists idx_feedback_session on feedback(session_id);
    create index if not exists idx_feedback_rating on feedback(rating);

    -- 5. product_events
    create table if not exists product_events (
        event_id uuid primary key,
        tenant_id text not null,
        user_id text,
        session_id text,
        event_name text not null,
        payload jsonb,
        occurred_at timestamptz not null default now()
    );
    create index if not exists idx_events_tenant_occurred on product_events(tenant_id, occurred_at);
    create index if not exists idx_events_session on product_events(session_id);
    create index if not exists idx_events_name on product_events(event_name);

    -- 6. reports
    create table if not exists reports (
        report_id uuid primary key,
        session_id text not null,
        report_type text not null,
        html text not null,
        pdf_path text,
        created_at timestamptz not null default now()
    );
    create index if not exists idx_reports_session on reports(session_id);
    """)

def downgrade() -> None:
    op.execute("""
    drop table if exists reports;
    drop table if exists product_events;
    drop table if exists feedback;
    drop table if exists simulation_turns;

    drop index if exists idx_reports_session;
    drop index if exists idx_events_name;
    drop index if exists idx_events_session;
    drop index if exists idx_events_tenant_occurred;
    drop index if exists idx_feedback_rating;
    drop index if exists idx_feedback_session;
    drop index if exists idx_feedback_tenant;
    drop index if exists idx_turns_session_number;
    drop index if exists idx_sessions_status;
    drop index if exists idx_sessions_scenario;
    drop index if exists idx_sessions_tenant_started;

    alter table simulation_sessions
        drop column if exists metadata,
        drop column if exists readiness_score,
        drop column if exists score,
        drop column if exists duration_ms,
        drop column if exists ended_at,
        drop column if exists started_at,
        drop column if exists procedure_id,
        drop column if exists persona_id;
    """)
