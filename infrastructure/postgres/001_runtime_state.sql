create table if not exists simulation_sessions (
    session_id text primary key,
    tenant_id text not null,
    learner_id text not null,
    scenario_id text not null,
    status text not null,
    payload jsonb not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists audit_events (
    audit_id text primary key,
    event_type text not null,
    tenant_id text not null,
    aggregate_type text not null,
    aggregate_id text not null,
    occurred_at timestamptz not null,
    trace_id text not null,
    actor_id text,
    payload jsonb not null
);

create index if not exists audit_events_aggregate_idx
    on audit_events (aggregate_type, aggregate_id, occurred_at);

create index if not exists audit_events_tenant_idx
    on audit_events (tenant_id, occurred_at);

create table if not exists tenants (
    tenant_id text primary key,
    name text not null,
    environment text not null,
    created_at timestamptz not null default now()
);

create table if not exists identity_users (
    tenant_id text not null references tenants (tenant_id),
    user_id text not null,
    email text not null,
    display_name text not null,
    roles jsonb not null,
    password_hash text not null,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (tenant_id, user_id)
);

create unique index if not exists identity_users_tenant_email_idx
    on identity_users (tenant_id, lower(email));
