from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytest
from callibr_contracts import (
    ConversationContext,
    ConversationResult,
    ConversationState,
    ConversationTurn,
    ModelRequest,
    ProcedureDefinition,
    RuleAction,
    RuleCondition,
    RuleDefinition,
    ScenarioDefinition,
    ScenarioMetadata,
    ScenarioReference,
    StepDefinition,
)
from callibr_contracts.persona import (
    PersonaCommunication,
    PersonaDefinition,
    PersonaMemoryProfile,
)
from callibr_contracts.persona import (
    PersonaMetadata as PersonaMeta,
)
from callibr_conversation import (
    ContextBuilder,
    ConversationService,
    MockAdapter,
    SessionMemory,
    SessionNotFoundError,
    TurnMemory,
)
from callibr_kernel import EventBus
from callibr_persistence import (
    InMemoryConversationStore,
    InMemoryPersonaDefinitionStore,
    InMemoryProcedureStore,
    InMemoryRuleStore,
    InMemoryTransactionManager,
)
from callibr_persistence.scenario_store import InMemoryScenarioDefinitionStore
from callibr_persona import PersonaRegistry, PersonaService, PersonaValidator
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_rule import RuleRegistry, RuleService, RuleValidator
from callibr_scenario import (
    ScenarioRegistry,
    ScenarioService,
    ScenarioValidator,
)


class _InMemoryAuditStore:
    def __init__(self) -> None:
        self.records: list[Any] = []

    def append(self, record: Any) -> None:
        self.records.append(record)

    def list_by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[Any]:
        return [
            r
            for r in self.records
            if r.aggregate_type == aggregate_type and r.aggregate_id == aggregate_id
        ]


def conversation_service() -> ConversationService:
    event_bus = EventBus()
    audit_store = _InMemoryAuditStore()

    procedure_registry = ProcedureRegistry()
    procedure_executor = ProcedureExecutor()
    procedure_store = InMemoryProcedureStore()
    procedure_service = ProcedureService(
        registry=procedure_registry,
        executor=procedure_executor,
        store=procedure_store,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )

    proc = ProcedureDefinition(
        procedure_id="sales-qualification",
        version="1.0.0",
        name="Sales Qualification",
        steps=[StepDefinition(step_id="greeting", type="greeting", title="Greeting")],
    )
    procedure_service.define(proc)

    scenario_registry = ScenarioRegistry()
    scenario_validator = ScenarioValidator(
        procedure_registry=procedure_registry,
    )
    scenario_store = InMemoryScenarioDefinitionStore()
    scenario_service = ScenarioService(
        registry=scenario_registry,
        validator=scenario_validator,
        store=scenario_store,
        procedure_service=procedure_service,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )

    scenario = ScenarioDefinition(
        scenario_id="qualification-call",
        name="Qualification Call",
        reference=ScenarioReference(
            procedure_id="sales-qualification",
            persona_id="senior-sales-manager",
        ),
        metadata=ScenarioMetadata(),
    )
    scenario_service.define(scenario)

    persona_registry = PersonaRegistry()
    persona_validator = PersonaValidator()
    persona_store = InMemoryPersonaDefinitionStore()
    persona_service = PersonaService(
        registry=persona_registry,
        validator=persona_validator,
        store=persona_store,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )

    persona = PersonaDefinition(
        persona_id="senior-sales-manager",
        name="Senior Sales Manager",
        description="Commercial expérimenté B2B",
        role="Sales Manager",
        tone=["professionnel"],
        communication=PersonaCommunication(
            style="consultatif",
            verbosity="medium",
            language="fr",
        ),
        memory_profile=PersonaMemoryProfile(),
        metadata=PersonaMeta(),
    )
    persona_service.define(persona)

    rule_registry = RuleRegistry()
    rule_validator = RuleValidator()
    rule_store = InMemoryRuleStore()
    rule_service = RuleService(
        registry=rule_registry,
        validator=rule_validator,
        store=rule_store,
        audit_event_store=audit_store,
        event_bus=event_bus,
    )

    rule_service.define(
        RuleDefinition(
            rule_id="welcome-bonus",
            name="Welcome Bonus",
            priority=100,
            conditions=[
                RuleCondition(condition_id="is-new", type="exists", field="new_user"),
            ],
            actions=[
                RuleAction(action_id="add-score", type="add_score", value=5.0),
            ],
        )
    )

    from callibr_crm import CrmActionService
    from callibr_evaluation import EvaluationService

    crm_service = CrmActionService()
    eval_service = EvaluationService()
    mock_llm = MockAdapter(response_text="Bonjour, comment puis-je vous aider aujourd'hui ?")

    return ConversationService(
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
    )


class TestMemory:
    def test_turn_memory_add_and_retrieve(self) -> None:
        mem = TurnMemory()
        turn = mem.add_turn("user", "Bonjour")
        assert turn.role == "user"
        assert turn.content == "Bonjour"
        assert turn.turn_id.startswith("turn_")
        assert len(mem.get_turns()) == 1

    def test_turn_memory_last_turn(self) -> None:
        mem = TurnMemory()
        mem.add_turn("user", "Hello")
        mem.add_turn("assistant", "Hi")
        last = mem.last_turn()
        assert last is not None
        assert last.content == "Hi"

    def test_turn_memory_clear(self) -> None:
        mem = TurnMemory()
        mem.add_turn("user", "Hello")
        mem.clear()
        assert len(mem.get_turns()) == 0

    def test_session_memory(self) -> None:
        mem = SessionMemory("session-1")
        mem.add_turn("user", "Hello")
        mem.set_variable("key", "value")
        state = mem.to_state()
        assert state.session_id == "session-1"
        assert len(state.turns) == 1
        assert state.variables["key"] == "value"


class TestContextAssembly:
    def test_build_system_context_with_blocked(self) -> None:
        from callibr_contracts import RuleEvaluation, RuleMatch

        eval_ = RuleEvaluation(
            results=[RuleMatch(rule_id="r1", rule_name="R1", matched=False, priority=0)],
            blocked=True,
        )
        builder = ContextBuilder()
        ctx = builder.build_system_context(rule_eval=eval_)
        assert "bloquées" in ctx

    def test_assemble_context_with_full_data(self) -> None:
        plan = type(
            "Plan",
            (),
            {
                "execution_context": {"procedure_id": "p1"},
            },
        )()
        from callibr_contracts import PromptContext

        prompt = PromptContext(persona_prompt="Tu es un assistant.")
        state = ConversationState(
            session_id="s1",
            correlation_id=uuid4(),
            turns=[
                ConversationTurn(
                    turn_id="t1",
                    role="user",
                    content="Hi",
                    timestamp=datetime(2024, 1, 1),
                )
            ],
            started_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 1, 1),
        )
        builder = ContextBuilder()
        ctx = builder.assemble_context(plan=plan, prompt_ctx=prompt, state=state)
        assert ctx.persona_context.persona_prompt == "Tu es un assistant."
        assert len(ctx.conversation_state.turns) == 1

    def test_build_model_request_includes_turns(self) -> None:
        from callibr_contracts import ConversationMetadata, PromptContext

        state = ConversationState(
            session_id="s1",
            correlation_id=uuid4(),
            turns=[
                ConversationTurn(
                    turn_id="t1",
                    role="assistant",
                    content="Bonjour",
                    timestamp=datetime(2024, 1, 1),
                ),
            ],
            started_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 1, 1),
        )
        ctx = ConversationContext(
            persona_context=PromptContext(persona_prompt="Tu es un assistant."),
            conversation_state=state,
            metadata=ConversationMetadata(),
        )
        builder = ContextBuilder()
        req = builder.build_model_request(ctx, "Nouveau message")
        assert len(req.messages) == 3
        assert req.messages[0]["role"] == "system"
        assert req.messages[1]["role"] == "assistant"
        assert req.messages[1]["content"] == "Bonjour"
        assert req.messages[2]["role"] == "user"


class TestPipeline:
    def test_start_conversation_returns_context(self) -> None:
        service = conversation_service()
        result = service.start_conversation("qualification-call")
        assert isinstance(result, ConversationResult)
        assert isinstance(result.context, ConversationContext)
        assert isinstance(result.state, ConversationState)

    def test_process_message_returns_response(self) -> None:
        service = conversation_service()
        start = service.start_conversation("qualification-call")
        result = service.process_message(start.state.session_id, "Bonjour")
        assert "Bonjour" in result.response.content or "puis-je" in result.response.content
        assert len(result.state.turns) == 2

    def test_process_message_invalid_session_raises(self) -> None:
        service = conversation_service()
        with pytest.raises(SessionNotFoundError):
            service.process_message("invalid-session", "Hello")

    def test_get_session_state(self) -> None:
        service = conversation_service()
        start = service.start_conversation("qualification-call")
        state = service.get_session_state(start.state.session_id)
        assert isinstance(state, ConversationState)

    def test_get_session_state_invalid_raises(self) -> None:
        service = conversation_service()
        with pytest.raises(SessionNotFoundError):
            service.get_session_state("invalid")


class TestMockAdapter:
    def test_mock_adapter_returns_expected_text(self) -> None:
        adapter = MockAdapter(response_text="Réponse test")
        req = ModelRequest(messages=[{"role": "user", "content": "Hi"}])
        resp = adapter.generate(req)
        assert resp.content == "Réponse test"
        assert resp.model_id == "mock"

    def test_mock_adapter_tracks_calls(self) -> None:
        adapter = MockAdapter()
        req = ModelRequest(messages=[])
        adapter.generate(req)
        adapter.generate(req)
        assert adapter.call_count == 2

    def test_mock_adapter_health(self) -> None:
        adapter = MockAdapter()
        assert adapter.health() is True

    def test_mock_adapter_metadata(self) -> None:
        adapter = MockAdapter()
        meta = adapter.metadata()
        assert meta["model_id"] == "mock"
