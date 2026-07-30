"""Tests unitaires — S13 Transactional Outbox & Durable Events."""

from __future__ import annotations

import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from callibr_contracts import (
    DomainEvent,
    OutboxRecord,
    OutboxStatus,
)
from callibr_conversation import ConversationService, MockAdapter
from callibr_crm import CrmActionService
from callibr_evaluation import EvaluationService
from callibr_kernel import EventBus
from callibr_kernel.time import utc_now
from callibr_persistence import (
    InMemoryAuditEventStore,
    InMemoryConversationStore,
    InMemoryOutboxStore,
    InMemoryPersonaDefinitionStore,
    InMemoryProcedureStore,
    InMemoryRuleStore,
    InMemoryScenarioDefinitionStore,
    InMemoryTransactionManager,
    OutboxPublisher,
)
from callibr_persona import PersonaRegistry, PersonaService, PersonaValidator
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_rule import RuleRegistry, RuleService, RuleValidator
from callibr_scenario import ScenarioRegistry, ScenarioService, ScenarioValidator
from callibr_seed import load_demo_catalogue


# ---------------------------------------------------------------------------
# TestDomainEvent — Immutable & Defaults
# ---------------------------------------------------------------------------
class TestDomainEvent:
    def test_domain_event_is_immutable(self) -> None:
        event = DomainEvent(
            event_type="test.occurred",
            aggregate_type="test",
            aggregate_id="123",
            aggregate_version=1,
            tenant_id="t1",
            correlation_id=uuid4(),
            payload={"foo": "bar"},
        )
        import pydantic

        with pytest.raises(pydantic.ValidationError):
            event.aggregate_version = 2

    def test_domain_event_defaults(self) -> None:
        event = DomainEvent(
            event_type="test",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        assert isinstance(event.event_id, UUID)
        assert isinstance(event.occurred_at, datetime.datetime)
        assert event.causation_id is None
        assert event.payload == {}
        assert event.metadata == {}


# ---------------------------------------------------------------------------
# TestOutboxRecord — Mappings
# ---------------------------------------------------------------------------
class TestOutboxRecord:
    def test_outbox_record_defaults(self) -> None:
        event = DomainEvent(
            event_type="test",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        record = OutboxRecord.from_event(event)
        assert record.status == OutboxStatus.PENDING
        assert record.attempt_count == 0
        assert record.last_error is None
        assert record.published_at is None
        assert record.event_id == event.event_id


# ---------------------------------------------------------------------------
# TestOutboxStore (InMemory)
# ---------------------------------------------------------------------------
class TestOutboxStore:
    def test_append_and_claim_pending(self) -> None:
        store = InMemoryOutboxStore()
        event1 = DomainEvent(
            event_type="e1",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        event2 = DomainEvent(
            event_type="e2",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=2,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event1)
        store.append(event2)

        pending = store.claim_pending(limit=10, worker_id="w1")
        assert len(pending) == 2
        assert pending[0].event_id == event1.event_id

    def test_idempotent_publish(self) -> None:
        store = InMemoryOutboxStore()
        event = DomainEvent(
            event_type="e",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event)
        store.append(event)  # Should not duplicate

        pending = store.claim_pending(limit=10, worker_id="w1")
        assert len(pending) == 1

    def test_mark_published(self) -> None:
        store = InMemoryOutboxStore()
        event = DomainEvent(
            event_type="e",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event)

        now = utc_now()
        store.mark_published(event.event_id, now)

        pending = store.claim_pending(limit=10, worker_id="w1")
        assert len(pending) == 0
        assert store._records[event.event_id].status == OutboxStatus.PUBLISHED
        assert store._records[event.event_id].published_at == now

    def test_mark_failed(self) -> None:
        store = InMemoryOutboxStore()
        event = DomainEvent(
            event_type="e",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event)

        # Claim first (normal flow: claim_pending increments attempt_count)
        records = store.claim_pending(limit=10, worker_id="w1")
        assert len(records) == 1
        assert records[0].attempt_count == 1

        store.mark_failed(event.event_id, "connection error")

        pending = store.claim_pending(limit=10, worker_id="w1")
        assert len(pending) == 0
        record = store._records[event.event_id]
        assert record.status == OutboxStatus.FAILED
        assert record.last_error == "connection error"
        assert record.attempt_count == 1


# ---------------------------------------------------------------------------
# TestOutboxPublisher
# ---------------------------------------------------------------------------
class TestOutboxPublisher:
    def test_publisher_claims_batch_and_publishes(self) -> None:
        store = InMemoryOutboxStore()
        mock_event_publisher = MagicMock()
        publisher = OutboxPublisher(store=store, publisher=mock_event_publisher)

        event = DomainEvent(
            event_type="e",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event)

        published_count = publisher.publish_pending(limit=10)

        assert published_count == 1
        assert mock_event_publisher.publish.call_count == 1
        published_event = mock_event_publisher.publish.call_args[0][0]
        assert published_event.event_id == event.event_id

        pending = store.claim_pending(limit=10, worker_id="w1")
        assert len(pending) == 0
        assert store._records[event.event_id].status == OutboxStatus.PUBLISHED

    def test_retry_bounded_and_error_persisted(self) -> None:
        store = InMemoryOutboxStore()
        mock_event_publisher = MagicMock()
        mock_event_publisher.publish.side_effect = Exception("network fail")
        publisher = OutboxPublisher(store=store, publisher=mock_event_publisher, max_retries=2)

        event = DomainEvent(
            event_type="e",
            aggregate_type="a",
            aggregate_id="1",
            aggregate_version=1,
            tenant_id="t",
            correlation_id=uuid4(),
        )
        store.append(event)

        # Attempt 1 -> fails
        count = publisher.publish_pending()
        assert count == 0

        # Reset back to pending for retry; clear next_attempt_at so claim_pending picks it up
        store._records[event.event_id] = store._records[event.event_id].model_copy(
            update={"status": OutboxStatus.PENDING, "next_attempt_at": None}
        )

        # Attempt 2 -> fails
        count = publisher.publish_pending()
        assert count == 0

        store._records[event.event_id] = store._records[event.event_id].model_copy(
            update={"status": OutboxStatus.PENDING, "next_attempt_at": None}
        )

        # Attempt 3 -> hits max retries
        count = publisher.publish_pending()
        assert count == 0

        # Check attempts
        record = store._records[event.event_id]
        assert record.attempt_count == 3
        assert record.status == OutboxStatus.FAILED

        # Verify it wasn't even called on the 3rd attempt because attempt_count == max_retries
        assert mock_event_publisher.publish.call_count == 2


# ---------------------------------------------------------------------------
# TestVerticalSlice
# ---------------------------------------------------------------------------
class TestVerticalSlice:
    def _setup_services(self) -> tuple[ConversationService, InMemoryOutboxStore]:
        event_bus = EventBus()
        audit_store = InMemoryAuditEventStore()
        outbox_store = InMemoryOutboxStore()

        procedure_service = ProcedureService(
            registry=ProcedureRegistry(),
            executor=ProcedureExecutor(),
            store=InMemoryProcedureStore(),
            audit_event_store=audit_store,
            event_bus=event_bus,
        )

        scenario_service = ScenarioService(
            registry=ScenarioRegistry(),
            validator=ScenarioValidator(procedure_registry=procedure_service._registry),
            store=InMemoryScenarioDefinitionStore(),
            procedure_service=procedure_service,
            audit_event_store=audit_store,
            event_bus=event_bus,
        )

        persona_service = PersonaService(
            registry=PersonaRegistry(),
            validator=PersonaValidator(),
            store=InMemoryPersonaDefinitionStore(),
            audit_event_store=audit_store,
            event_bus=event_bus,
        )

        rule_service = RuleService(
            registry=RuleRegistry(),
            validator=RuleValidator(),
            store=InMemoryRuleStore(),
            audit_event_store=audit_store,
            event_bus=event_bus,
        )

        load_demo_catalogue(
            persona_service=persona_service,
            procedure_service=procedure_service,
            rule_service=rule_service,
            scenario_service=scenario_service,
        )

        crm_service = CrmActionService()
        eval_service = EvaluationService()
        mock_llm = MockAdapter(response_text="Mock response")

        conversation_service = ConversationService(
            scenario_service=scenario_service,
            procedure_service=procedure_service,
            persona_service=persona_service,
            rule_service=rule_service,
            evaluation_service=eval_service,
            crm_service=crm_service,
            llm_adapter=mock_llm,
            event_bus=event_bus,
            transaction_manager=InMemoryTransactionManager(),
            conversation_store=InMemoryConversationStore(),
            outbox_store=outbox_store,
        )

        return conversation_service, outbox_store

    def test_conversation_events_are_written_to_outbox(self) -> None:
        conversation_service, outbox_store = self._setup_services()

        # 1. Start Conversation -> Should emit 'conversation.started'
        start_result = conversation_service.start_conversation("sc-sav-retard-colis-v1")
        session_id = start_result.state.session_id

        records = outbox_store.claim_pending(limit=10, worker_id="w1")
        assert len(records) == 1
        assert records[0].event_type == "conversation.started"
        assert records[0].aggregate_id == session_id

        # Clear for next check by marking published
        outbox_store.mark_published(records[0].event_id, utc_now())

        # 2. Process Message -> Should emit 'turn.completed'
        conversation_service.process_message(session_id, "Hello")

        records2 = outbox_store.claim_pending(limit=10, worker_id="w1")
        assert len(records2) == 1
        assert records2[0].event_type == "turn.completed"
        assert records2[0].aggregate_id == session_id
        assert records2[0].payload["turn_count"] == 2
