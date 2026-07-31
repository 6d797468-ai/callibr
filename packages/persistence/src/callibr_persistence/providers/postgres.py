from callibr_persistence.providers.base import PersistenceProvider
from callibr_persistence.postgres.simulation_turn_store import PostgresSimulationTurnStore
from callibr_persistence.postgres.simulation_session_store import PostgresSimulationSessionStore
from callibr_persistence.postgres.conversation_store import PostgresConversationStore
from callibr_persistence.postgres.feedback_store import PostgresFeedbackStore
from callibr_persistence.postgres.product_event_store import PostgresProductEventStore
from callibr_persistence.postgres.report_store import PostgresReportStore

class PostgresPersistenceProvider(PersistenceProvider):
    def __init__(self, db_url: str) -> None:
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
