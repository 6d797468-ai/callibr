"""Create pilot persistence tables

Revision ID: 005
Revises: 004
Create Date: 2026-07-31 10:00:00.000000

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
    -- ENUM types
    create type simulation_status as enum ('started', 'running', 'completed', 'cancelled', 'failed');
    create type speaker_type as enum ('learner', 'customer', 'system', 'coach');

    -- 1. simulation_sessions
    create table if not exists simulation_sessions (
        session_id uuid primary key,
        tenant_id text not null,
        scenario_id text not null,
        persona_id text,
        procedure_id text,
        status simulation_status not null,
        started_at timestamptz not null,
        ended_at timestamptz,
        duration_ms bigint,
        score numeric(5,2),
        readiness_score numeric(5,2),
        metadata jsonb,
        created_at timestamptz not null default now(),
        updated_at timestamptz not null default now()
    );
    create index if not exists idx_sessions_tenant_started on simulation_sessions(tenant_id, started_at);
    create index if not exists idx_sessions_scenario on simulation_sessions(scenario_id);
    create index if not exists idx_sessions_status on simulation_sessions(status);

    -- 2. simulation_turns
    create table if not exists simulation_turns (
        turn_id uuid primary key,
        session_id uuid not null references simulation_sessions(session_id),
        turn_number integer not null,
        speaker speaker_type not null,
        message text not null,
        evaluation jsonb,
        created_at timestamptz not null default now(),
        unique(session_id, turn_number)
    );
    create index if not exists idx_turns_session_number on simulation_turns(session_id, turn_number);

    -- 3. feedback
    create table if not exists feedback (
        feedback_id uuid primary key,
        session_id uuid not null references simulation_sessions(session_id),
        tenant_id text not null,
        rating integer not null check (rating between 1 and 5),
        would_recommend boolean,
        comment text,
        created_at timestamptz not null default now()
    );
    create index if not exists idx_feedback_tenant on feedback(tenant_id);
    create index if not exists idx_feedback_session on feedback(session_id);
    create index if not exists idx_feedback_rating on feedback(rating);

    -- 4. product_events
    create table if not exists product_events (
        event_id uuid primary key,
        tenant_id text not null,
        user_id text,
        session_id uuid,
        event_name text not null,
        payload jsonb,
        occurred_at timestamptz not null default now()
    );
    create index if not exists idx_events_tenant_occurred on product_events(tenant_id, occurred_at);
    create index if not exists idx_events_session on product_events(session_id);
    create index if not exists idx_events_name on product_events(event_name);

    -- 5. reports
    create table if not exists reports (
        report_id uuid primary key,
        session_id uuid not null references simulation_sessions(session_id),
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
    drop table if exists simulation_sessions;
    drop type if exists speaker_type;
    drop type if exists simulation_status;
    """)
