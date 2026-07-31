from callibr_persistence.providers.base import PersistenceProvider
from callibr_persistence.conversation_store import InMemoryConversationStore
from callibr_persistence.session_store import InMemorySimulationSessionStore
from callibr_persistence.memory.simulation_turn_store import MemorySimulationTurnStore
from callibr_persistence.memory.feedback_store import MemoryFeedbackStore
from callibr_persistence.memory.product_event_store import MemoryProductEventStore
from callibr_persistence.memory.report_store import MemoryReportStore

class MemoryPersistenceProvider(PersistenceProvider):
    def __init__(self) -> None:
        super().__init__(
            conversation_store=InMemoryConversationStore(),
            simulation_store=InMemorySimulationSessionStore(),
            turn_store=MemorySimulationTurnStore(),
            feedback_store=MemoryFeedbackStore(),
            analytics_store=MemoryProductEventStore(),
            report_store=MemoryReportStore(),
        )
