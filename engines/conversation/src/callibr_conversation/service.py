"""Conversation Runtime Service — Full pipeline orchestrator."""

from __future__ import annotations

import logging
from typing import Any

from callibr_contracts import (
    ConversationContext,
    ConversationMetadata,
    ConversationResult,
    ConversationState,
    ConversationStore,
    DomainEvent,
    ExecutionContext,
    LLMAdapter,
    LLMRouter,
    ModelResponse,
    OutboxStore,
    TokenBudget,
    TransactionManager,
)
from callibr_crm import CrmActionService
from callibr_evaluation import EvaluationService
from callibr_kernel import CallibrError, EventBus, new_id
from callibr_persona import PersonaService
from callibr_planning import ResponsePlan as CallibrResponsePlan
from callibr_procedure import ProcedureService
from callibr_rule import RuleService
from callibr_scenario import ScenarioService

from callibr_conversation.errors import SafetyViolationError, TokenBudgetExceededError
from callibr_conversation.events import ConversationEvent
from callibr_conversation.memory import SessionMemory
from callibr_conversation.orchestrator import ContextBuilder

log = logging.getLogger(__name__)


class SessionNotFoundError(CallibrError):
    def __init__(self, session_id: str) -> None:
        super().__init__(
            "SESSION_NOT_FOUND",
            f"Conversation session {session_id} was not found.",
            details={"session_id": session_id},
        )


class ConversationService:
    def __init__(
        self,
        scenario_service: ScenarioService,
        procedure_service: ProcedureService,
        persona_service: PersonaService,
        rule_service: RuleService,
        evaluation_service: EvaluationService,
        crm_service: CrmActionService,
        llm_adapter: LLMAdapter | None = None,
        event_bus: EventBus | None = None,
        transaction_manager: TransactionManager | None = None,
        conversation_store: ConversationStore | None = None,
        outbox_store: OutboxStore | None = None,
        budget_evaluator: Any | None = None,
        safety_validator: Any | None = None,
        context_reducer: Any | None = None,
        llm_router: LLMRouter | None = None,
        token_budget: TokenBudget | None = None,
    ) -> None:
        self._scenario_service = scenario_service
        self._procedure_service = procedure_service
        self._persona_service = persona_service
        self._rule_service = rule_service
        self._evaluation_service = evaluation_service
        self._crm_service = crm_service
        self._llm_adapter = llm_adapter
        self._event_bus = event_bus
        self._transaction_manager = transaction_manager
        self._conversation_store = conversation_store
        self._outbox_store = outbox_store
        self._budget_evaluator = budget_evaluator
        self._safety_validator = safety_validator
        self._context_reducer = context_reducer
        self._llm_router = llm_router
        self._token_budget = token_budget
        self._context_builder = ContextBuilder()

    def start_conversation(
        self,
        scenario_id: str,
        tenant_id: str = "tenant_demo",
        actor_id: str = "learner_demo",
        extra_context: dict[str, Any] | None = None,
    ) -> ConversationResult:
        session_id = new_id("conv")
        session = SessionMemory(session_id)
        session.increment_version()

        plan = self._scenario_service.compose(
            scenario_id,
            tenant_id,
            actor_id,
            extra_context,
        )

        execution = self._procedure_service.start(
            type(
                "req",
                (),
                {
                    "procedure_id": plan.scenario.reference.procedure_id,
                    "tenant_id": tenant_id,
                    "actor_id": actor_id,
                    "initial_context": plan.execution_context,
                },
            )()
        )

        persona_id = plan.scenario.reference.persona_id
        self._persona_service.build_runtime(persona_id)
        prompt_ctx = self._persona_service.build_prompt_context(
            persona_id,
            scenario_context=plan.execution_context,
            procedure_context={"execution_id": execution.execution_id},
        )

        rule_ctx = ExecutionContext(
            variables=plan.execution_context,
            tenant_id=tenant_id,
            actor_id=actor_id,
            procedure_id=execution.procedure_id,
            scenario_id=scenario_id,
            persona_id=persona_id,
        )
        rule_eval = self._rule_service.evaluate(context=rule_ctx)

        metadata = ConversationMetadata(
            tenant_id=tenant_id,
            actor_id=actor_id,
            scenario_id=scenario_id,
            procedure_id=execution.procedure_id,
            execution_id=execution.execution_id,
            persona_id=persona_id,
        )

        session.set_variable("tenant_id", tenant_id)
        session.set_variable("actor_id", actor_id)

        state = session.to_state()
        ctx = self._context_builder.assemble_context(
            plan=plan,
            prompt_ctx=prompt_ctx,
            rule_eval=rule_eval,
            state=state,
            metadata=metadata,
        )

        with self._transaction_manager.transaction() as conn:
            self._conversation_store.save(state, conn=conn)
            self._publish(
                "conversation.started",
                session,
                tenant_id,
                {
                    "scenario_id": scenario_id,
                    "persona_id": persona_id,
                },
                conn=conn,
            )

        return ConversationResult(
            context=ctx,
            response=ModelResponse(content="", model_id="mock"),
            state=state,
        )

    def process_message(
        self,
        session_id: str,
        message: str,
        response_plan: CallibrResponsePlan | None = None,
    ) -> ConversationResult:
        state = self._conversation_store.get(session_id)
        if state is None:
            raise SessionNotFoundError(session_id)

        session = SessionMemory.from_state(state)
        session.add_turn("user", message)
        session.increment_version()

        state = session.to_state()
        ctx = self._rebuild_context(session, state)
        if response_plan is not None:
            plan_str = self._format_plan(response_plan)
            ctx = ConversationContext(  # noqa: PIE794
                system_context=ctx.system_context,
                persona_context=ctx.persona_context,
                scenario_context=ctx.scenario_context,
                procedure_context=ctx.procedure_context,
                rule_context=ctx.rule_context,
                crm_context=ctx.crm_context,
                memory_context=ctx.memory_context,
                evaluation_context=ctx.evaluation_context,
                plan_context=plan_str,
                metadata=ctx.metadata,
                conversation_state=ctx.conversation_state,
            )

        gen_request = self._manage_budget(ctx, message)

        self._check_safety_input(gen_request)

        adapter = self._resolve_adapter(gen_request)
        response = adapter.generate(gen_request)

        self._check_safety_output(response)

        session.add_turn("assistant", response.content)
        session.increment_version()
        updated_state = session.to_state()

        with self._transaction_manager.transaction() as conn:
            self._conversation_store.save(updated_state, conn=conn)
            self._publish(
                "turn.completed",
                session,
                ctx.metadata.tenant_id,
                {"turn_count": len(session.get_turns())},
                conn=conn,
            )

        return ConversationResult(
            context=ctx,
            response=response,
            state=updated_state,
        )

    def get_session_state(self, session_id: str) -> ConversationState:
        state = self._conversation_store.get(session_id)
        if state is None:
            raise SessionNotFoundError(session_id)
        return state

    def _format_plan(self, plan: CallibrResponsePlan) -> str:
        goals = ", ".join(g.value for g in plan.goals)
        return (
            f"--- Plan de réponse ---\n"
            f"Intention: {plan.intent.value}\n"
            f"Objectifs: {goals}\n"
            f"Ton: {plan.tone.value}\n"
            f"Style vocal: {plan.voice.value}\n"
            f"Contrainte: max {plan.constraints.max_sentences} phrases\n"
            f"Résultat attendu: {plan.expected_outcome}\n"
            f"---\n"
        )

    def _rebuild_context(
        self,
        session: SessionMemory,
        state: ConversationState,
    ) -> ConversationContext:
        metadata = ConversationMetadata(
            tenant_id=state.variables.get("tenant_id", "tenant_demo"),
            actor_id=state.variables.get("actor_id", "learner_demo"),
        )
        return ConversationContext(
            memory_context={
                "turn_count": len(state.turns),
                "last_turn": state.turns[-1].content if state.turns else "",
            },
            metadata=metadata,
            conversation_state=state,
        )

    def _manage_budget(self, ctx: ConversationContext, message: str) -> Any:
        if self._budget_evaluator is None or self._token_budget is None:
            return self._context_builder.build_model_request(ctx, message)

        from callibr_telemetry import budget_evaluation_total, context_reduction_total

        req = self._context_builder.build_model_request(ctx, message)
        result = self._budget_evaluator.evaluate(req, self._token_budget)

        if result.within_budget:
            budget_evaluation_total.labels(within_budget="true").inc()
            return req

        budget_evaluation_total.labels(within_budget="false").inc()

        if self._context_reducer is None:
            raise TokenBudgetExceededError(
                available_tokens=self._token_budget.available_input_tokens,
                required_tokens=result.usage.total_input_tokens,
            )

        reduced = self._context_reducer.reduce(ctx, self._token_budget)
        context_reduction_total.labels(reduced="true").inc()

        new_req = self._context_builder.build_model_request(reduced, message)
        re_result = self._budget_evaluator.evaluate(new_req, self._token_budget)
        if not re_result.within_budget:
            raise TokenBudgetExceededError(
                available_tokens=self._token_budget.available_input_tokens,
                required_tokens=re_result.usage.total_input_tokens,
            )

        return new_req

    def _check_safety_input(self, request: Any) -> None:
        if self._safety_validator is None:
            return

        result = self._safety_validator.validate_input(request)
        from callibr_telemetry import safety_validation_total

        if not result.is_safe:
            safety_validation_total.labels(
                direction="input", verdict="blocked"
            ).inc()
            raise SafetyViolationError(
                direction="input",
                reason=result.reason or "Unknown safety violation",
                categories=result.flagged_categories,
            )

        safety_validation_total.labels(
            direction="input", verdict="allowed"
        ).inc()

    def _check_safety_output(self, response: ModelResponse) -> None:
        if self._safety_validator is None:
            return

        result = self._safety_validator.validate_output(response)
        from callibr_telemetry import safety_validation_total

        if not result.is_safe:
            safety_validation_total.labels(
                direction="output", verdict="blocked"
            ).inc()
            raise SafetyViolationError(
                direction="output",
                reason=result.reason or "Unknown safety violation",
                categories=result.flagged_categories,
            )

        safety_validation_total.labels(
            direction="output", verdict="allowed"
        ).inc()

    def _resolve_adapter(self, request: Any) -> LLMAdapter:
        if self._llm_router is not None:
            adapter = self._llm_router.select(request)
            meta = adapter.metadata()
            from callibr_telemetry import llm_routing_total
            llm_routing_total.labels(
                provider=meta.get("provider", "unknown"),
                model=meta.get("model_id", "unknown"),
                selected="true",
            ).inc()
            return adapter

        if self._llm_adapter is not None:
            meta = self._llm_adapter.metadata()
            from callibr_telemetry import llm_routing_total
            llm_routing_total.labels(
                provider=meta.get("provider", "unknown"),
                model=meta.get("model_id", "unknown"),
                selected="true",
            ).inc()
            return self._llm_adapter

        msg = "No LLM adapter or router configured."
        raise RuntimeError(msg)

    def _publish(
        self,
        event_type: str,
        session: SessionMemory,
        tenant_id: str,
        payload: dict[str, Any],
        conn: Any = None,
    ) -> None:
        if self._outbox_store:
            domain_event = DomainEvent(
                event_type=event_type,
                aggregate_type="conversation",
                aggregate_id=session.session_id,
                aggregate_version=session.to_state().version,
                tenant_id=tenant_id,
                correlation_id=session.correlation_id,
                payload=payload,
            )
            self._outbox_store.append(domain_event, conn=conn)

        self._event_bus.publish(
            ConversationEvent(
                event_type=event_type,
                session_id=session.session_id,
                tenant_id=tenant_id,
                payload=payload,
            )
        )
