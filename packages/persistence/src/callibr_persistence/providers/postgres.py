from callibr_persistence.postgres import normalize_psycopg_url
from callibr_persistence.postgres.conversation_store import PostgresConversationStore
from callibr_persistence.postgres.feedback_store import PostgresFeedbackStore
from callibr_persistence.postgres.product_event_store import PostgresProductEventStore
from callibr_persistence.postgres.report_store import PostgresReportStore
from callibr_persistence.postgres.simulation_session_store import PostgresSimulationSessionStore
from callibr_persistence.postgres.simulation_turn_store import PostgresSimulationTurnStore
from callibr_persistence.providers.base import PersistenceProvider


class PostgresPersistenceProvider(PersistenceProvider):
    def __init__(self, db_url: str) -> None:
        self._database_url = normalize_psycopg_url(db_url)
        turn_store = PostgresSimulationTurnStore(db_url)
        session_store = PostgresSimulationSessionStore(db_url)
        self._conversation_store = PostgresConversationStore(db_url)

        super().__init__(
            conversation_store=self._conversation_store,
            simulation_store=session_store,
            turn_store=turn_store,
            feedback_store=PostgresFeedbackStore(db_url),
            analytics_store=PostgresProductEventStore(db_url),
            report_store=PostgresReportStore(db_url),
        )

    def init_schema(self) -> None:
        self._conversation_store.init_schema()
        _create_tables(self._database_url)


def _create_tables(database_url: str) -> None:
    from psycopg import connect

    with connect(database_url) as connection:
        connection.execute(
            """
            create table if not exists simulation_sessions (
                session_id text primary key,
                tenant_id text not null,
                learner_id text,
                scenario_id text not null,
                status text not null,
                payload jsonb,
                persona_id text,
                procedure_id text,
                started_at timestamptz,
                ended_at timestamptz,
                duration_ms bigint,
                score numeric(5,2),
                readiness_score numeric(5,2),
                metadata jsonb,
                created_at timestamptz not null default now(),
                updated_at timestamptz not null default now()
            );

            alter table simulation_sessions
                add column if not exists persona_id text,
                add column if not exists procedure_id text,
                add column if not exists started_at timestamptz,
                add column if not exists ended_at timestamptz,
                add column if not exists duration_ms bigint,
                add column if not exists score numeric(5,2),
                add column if not exists readiness_score numeric(5,2),
                add column if not exists metadata jsonb;

            alter table simulation_sessions
                alter column learner_id drop not null,
                alter column payload drop not null;

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

            create table if not exists feedback (
                feedback_id uuid primary key,
                session_id text not null,
                tenant_id text not null,
                rating integer not null check (rating between 1 and 5),
                would_recommend boolean,
                comment text,
                created_at timestamptz not null default now()
            );

            create table if not exists product_events (
                event_id uuid primary key,
                tenant_id text not null,
                user_id text,
                session_id text,
                event_name text not null,
                payload jsonb,
                occurred_at timestamptz not null default now()
            );

            create table if not exists reports (
                report_id uuid primary key,
                session_id text not null,
                report_type text not null,
                html text not null,
                pdf_path text,
                created_at timestamptz not null default now()
            );
            """
        )
