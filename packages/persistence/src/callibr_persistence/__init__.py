"""Persistence adapters for Callibr runtime state."""

from callibr_contracts import AuditEventStore, SimulationSessionStore

from callibr_persistence.audit_store import (
    InMemoryAuditEventStore,
    PostgresAuditEventStore,
)
from callibr_persistence.conversation_store import (
    InMemoryConversationStore,
    PostgresConversationStore,
)
from callibr_persistence.identity_store import (
    IdentityStore,
    InMemoryIdentityStore,
    PostgresIdentityStore,
)
from callibr_persistence.outbox_publisher import (
    InProcessEventPublisher,
    OutboxPublisher,
)
from callibr_persistence.outbox_store import (
    InMemoryOutboxStore,
    PostgresOutboxStore,
)
from callibr_persistence.persona_store import (
    InMemoryPersonaDefinitionStore,
    PostgresPersonaDefinitionStore,
)
from callibr_persistence.procedure_store import (
    InMemoryProcedureStore,
    PostgresProcedureStore,
)
from callibr_persistence.rule_store import (
    InMemoryRuleStore,
    PostgresRuleStore,
)
from callibr_persistence.scenario_store import (
    InMemoryScenarioDefinitionStore,
    PostgresScenarioDefinitionStore,
)
from callibr_persistence.session_store import (
    InMemorySimulationSessionStore,
    PostgresSimulationSessionStore,
)
from callibr_persistence.transactions import (
    InMemoryTransactionManager,
    PostgresTransactionManager,
)

__all__ = [
    "AuditEventStore",
    "IdentityStore",
    "InMemoryAuditEventStore",
    "InMemoryConversationStore",
    "InMemoryIdentityStore",
    "InMemoryOutboxStore",
    "InMemoryPersonaDefinitionStore",
    "InMemoryProcedureStore",
    "InMemoryRuleStore",
    "InMemoryScenarioDefinitionStore",
    "InMemorySimulationSessionStore",
    "InMemoryTransactionManager",
    "InProcessEventPublisher",
    "OutboxPublisher",
    "PostgresAuditEventStore",
    "PostgresConversationStore",
    "PostgresIdentityStore",
    "PostgresOutboxStore",
    "PostgresPersonaDefinitionStore",
    "PostgresProcedureStore",
    "PostgresRuleStore",
    "PostgresScenarioDefinitionStore",
    "PostgresSimulationSessionStore",
    "PostgresTransactionManager",
    "SimulationSessionStore",
]
