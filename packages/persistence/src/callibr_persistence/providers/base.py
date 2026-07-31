from dataclasses import dataclass

from callibr_contracts.conversation import ConversationStore
from callibr_contracts.ports import SimulationSessionStore, SimulationTurnStore
from callibr_contracts.telemetry import FeedbackStore, ProductEventStore, ReportStore


@dataclass
class PersistenceProvider:
    conversation_store: ConversationStore
    simulation_store: SimulationSessionStore
    turn_store: SimulationTurnStore
    feedback_store: FeedbackStore
    analytics_store: ProductEventStore
    report_store: ReportStore
