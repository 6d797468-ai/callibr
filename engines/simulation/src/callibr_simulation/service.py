from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from callibr_contracts import (
    AuditEventStore,
    AuditRecord,
    CrmActionDefinition,
    ExecuteCrmActionRequest,
    ExecuteCrmActionResponse,
    ReplayTurn,
    ScenarioRepository,
    ScenarioSummary,
    SendMessageRequest,
    SendMessageResponse,
    SessionReplay,
    SessionReport,
    SimulationEvaluation,
    SimulationMessage,
    SimulationSession,
    SimulationSessionStore,
    StartSimulationRequest,
)
from callibr_crm import CrmActionService
from callibr_director import (
    ConversationDirector,
    ConversationStage,
    DirectorContext,
    DirectorDecision,
)
from callibr_evaluation import EvaluationService
from callibr_kernel import (
    CallibrError,
    Event,
    EventBus,
    TenantContext,
    new_id,
    new_trace_id,
    utc_now,
)
from callibr_planning import (
    PlanningContext,
    ResponsePlan,
    ResponsePlanner,
    ResponseValidator,
    ValidationResult,
)
from callibr_scenario import ScenarioDefinition
from callibr_telemetry.product import emit_product_event

if TYPE_CHECKING:
    from callibr_conversation import ConversationService

log = logging.getLogger(__name__)

# Maps simulation scenario IDs to Conversation Engine scenario IDs.
# When a mapping is present and a ConversationService is injected, the
# simulation bridge activates and delegates LLM response generation to
# the full Persona/Procedure/Rule pipeline.
SCENARIO_BRIDGE_MAP: dict[str, str] = {
    "sav-retard-colis-001": "sc-sav-retard-colis-v1",
    "sav-erreur-facturation-001": "sc-sav-erreur-facturation-v1",
    "com-refus-paiement-001": "sc-com-refus-paiement-v1",
    "com-annulation-commande-001": "sc-com-annulation-commande-v1",
    "sup-login-impossible-001": "sc-sup-login-impossible-v1",
    "sup-incident-reseau-001": "sc-sup-incident-reseau-v1",
    "rec-echeance-depassee-001": "sc-rec-echeance-depassee-v1",
    "rec-plan-remboursement-001": "sc-rec-plan-remboursement-v1",
}


class SimulationNotFoundError(CallibrError):
    def __init__(self, session_id: str) -> None:
        super().__init__(
            "SIMULATION_NOT_FOUND",
            f"Simulation session {session_id} was not found.",
            details={"session_id": session_id},
        )


class SimulationAccessForbiddenError(CallibrError):
    def __init__(self, session_id: str, tenant_id: str) -> None:
        super().__init__(
            "SIMULATION_ACCESS_FORBIDDEN",
            "Simulation session does not belong to the current tenant.",
            details={"session_id": session_id, "tenant_id": tenant_id},
        )


class SimulationService:
    def __init__(
        self,
        scenario_repository: ScenarioRepository,
        crm_action_service: CrmActionService,
        evaluation_service: EvaluationService,
        session_store: SimulationSessionStore,
        audit_event_store: AuditEventStore,
        event_bus: EventBus,
        conversation_service: ConversationService | None = None,
    ) -> None:
        self._scenario_repository = scenario_repository
        self._crm_action_service = crm_action_service
        self._evaluation_service = evaluation_service
        self._session_store = session_store
        self._audit_event_store = audit_event_store
        self._event_bus = event_bus
        self._conversation_service = conversation_service
        self._director = ConversationDirector()
        self._planner = ResponsePlanner()
        self._validator = ResponseValidator()
        self._validation_max_retries = 2

    def list_scenarios(self) -> list[ScenarioSummary]:
        return self._scenario_repository.list_scenarios()

    def start_session(
        self,
        request: StartSimulationRequest,
        context: TenantContext | None = None,
    ) -> SimulationSession:
        scenario = self._scenario_repository.get(request.scenario_id, request.tenant_id)
        session = SimulationSession(
            session_id=new_id("sim"),
            tenant_id=request.tenant_id,
            learner_id=request.learner_id,
            scenario=scenario.summary,
            status="active",
            current_step="opening",
            started_at=utc_now(),
            messages=[
                SimulationMessage(
                    role="customer",
                    content=scenario.opening_message,
                    at=utc_now(),
                    metadata={"source": "scenario_opening"},
                )
            ],
            crm_context=scenario.crm_context,
            customer_profile=(
                scenario.customer_profile
                if isinstance(scenario.customer_profile, dict)
                else {}
            ),
        )
        session = self._bridge_start(session, request, context)
        self._session_store.save(session)
        self._append_audit(
            "simulation.started",
            session,
            {
                "scenario_id": session.scenario.scenario_id,
                "learner_id": session.learner_id,
                "bridge_active": session.conversation_session_id is not None,
            },
            context,
        )
        self._event_bus.publish(
            Event(
                event_type="simulation.started",
                tenant_id=session.tenant_id,
                payload={
                    "session_id": session.session_id,
                    "scenario_id": session.scenario.scenario_id,
                    "learner_id": session.learner_id,
                },
            )
        )

        from callibr_telemetry import simulations_started_total

        tenant = context.tenant_id if context else "unknown"
        simulations_started_total.labels(
            tenant_id=tenant,
            scenario_id=request.scenario_id,
        ).inc()

        return session

    def _bridge_start(
        self,
        session: SimulationSession,
        request: StartSimulationRequest,
        context: TenantContext | None,
    ) -> SimulationSession:
        """Optionally start a ConversationService session for the bridge.

        When a mapping exists for the simulation scenario ID and a
        ConversationService has been injected, this method starts the
        conversation engine and records the resulting session/execution IDs
        inside the SimulationSession so that subsequent turns can use the
        full LLM/Persona/Procedure pipeline.
        """
        if self._conversation_service is None:
            return session
        engine_scenario_id = SCENARIO_BRIDGE_MAP.get(request.scenario_id)
        if engine_scenario_id is None:
            return session
        try:
            result = self._conversation_service.start_conversation(
                scenario_id=engine_scenario_id,
                tenant_id=request.tenant_id,
                actor_id=request.learner_id,
            )
            conv_session_id = result.state.session_id
            proc_exec_id = result.context.metadata.execution_id or None
            log.info(
                "simulation.bridge: conversation started — conv=%s proc_exec=%s",
                conv_session_id,
                proc_exec_id,
            )
            return session.model_copy(
                update={
                    "conversation_session_id": conv_session_id,
                    "procedure_execution_id": proc_exec_id,
                }
            )
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "simulation.bridge: failed to start conversation (%s) — falling back",
                exc,
            )
            return session

    def get_session(
        self,
        session_id: str,
        context: TenantContext | None = None,
    ) -> SimulationSession:
        session = self._session_store.get(session_id)
        if session is None:
            raise SimulationNotFoundError(session_id)
        self._assert_session_access(session, context)
        return session

    def get_replay(
        self,
        session_id: str,
        context: TenantContext | None = None,
    ) -> SessionReplay:
        session = self.get_session(session_id, context)
        turns: list[ReplayTurn] = []
        msgs = session.messages
        i = 0
        turn_idx = 0
        while i < len(msgs) - 1:
            if msgs[i].role == "learner":
                learner_msg = msgs[i]
                has_next = i + 1 < len(msgs)
                customer_msg = msgs[i + 1] if has_next and msgs[i + 1].role == "customer" else None
                if customer_msg is not None:
                    turns.append(
                        ReplayTurn(
                            turn_index=turn_idx,
                            learner_message=learner_msg.content,
                            customer_message=customer_msg.content,
                        )
                    )
                    turn_idx += 1
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        return SessionReplay(
            session_id=session.session_id,
            tenant_id=session.tenant_id,
            learner_id=session.learner_id,
            scenario=session.scenario,
            started_at=session.started_at,
            completed_at=session.completed_at,
            status=session.status,
            turns=turns,
        )

    def send_message(
        self,
        session_id: str,
        request: SendMessageRequest,
        context: TenantContext | None = None,
    ) -> SendMessageResponse:
        session = self.get_session(session_id, context)
        scenario = self._scenario_repository.get(session.scenario.scenario_id, session.tenant_id)
        learner_message = SimulationMessage(
            role="learner",
            content=request.content.strip(),
            at=utc_now(),
            metadata={"step": session.current_step},
        )
        learner_turn_count = self._count_messages(session, "learner") + 1
        evaluation = self._evaluation_service.evaluate_turn(request.content, scenario)

        director_decision, response_plan = self._run_planning(
            session, learner_turn_count, evaluation, request.content
        )

        customer_reply = self._bridge_customer_reply(
            session, scenario, learner_turn_count, evaluation, response_plan
        )
        customer_message = SimulationMessage(
            role="customer",
            content=customer_reply,
            at=utc_now(),
            metadata={
                "turn": learner_turn_count,
                "bridge": session.conversation_session_id is not None,
                "director_command": director_decision.command.value if director_decision else "",
                "director_stage": director_decision.next_stage.value if director_decision else "",
            },
        )
        messages = [*session.messages, learner_message, customer_message]
        status = "completed" if learner_turn_count >= 4 and evaluation.score >= 70 else "active"
        completed_at = utc_now() if status == "completed" else session.completed_at
        next_step = (
            director_decision.next_stage.value
            if director_decision
            else self._next_step(learner_turn_count, evaluation)
        )
        updated = session.model_copy(
            update={
                "status": status,
                "completed_at": completed_at,
                "current_step": next_step,
                "messages": messages,
                "evaluation": evaluation,
            }
        )
        self._session_store.save(updated)
        self._append_audit(
            "simulation.message_processed",
            updated,
            {
                "score": evaluation.score,
                "status": updated.status,
                "current_step": updated.current_step,
                "message_role": learner_message.role,
            },
            context,
        )
        self._event_bus.publish(
            Event(
                event_type="simulation.message_processed",
                tenant_id=session.tenant_id,
                payload={
                    "session_id": session.session_id,
                    "score": evaluation.score,
                    "status": updated.status,
                },
            )
        )
        if learner_turn_count == 1:
            emit_product_event(
                "FirstMessageSent",
                tenant_id=session.tenant_id,
                scenario_id=session.scenario.scenario_id,
                session_id=session.session_id,
            )
        if status == "completed":
            emit_product_event(
                "ConversationCompleted",
                tenant_id=session.tenant_id,
                scenario_id=session.scenario.scenario_id,
                session_id=session.session_id,
                duration=(utc_now() - session.started_at).total_seconds(),
            )
        return SendMessageResponse(
            session=updated,
            customer_message=customer_message,
            evaluation=evaluation,
        )

    def list_crm_actions(
        self,
        session_id: str,
        context: TenantContext | None = None,
    ) -> list[CrmActionDefinition]:
        session = self.get_session(session_id, context)
        return self._crm_action_service.list_actions(session.crm_context)

    def execute_crm_action(
        self,
        session_id: str,
        request: ExecuteCrmActionRequest,
        context: TenantContext | None = None,
    ) -> ExecuteCrmActionResponse:
        session = self.get_session(session_id, context)
        result = self._crm_action_service.execute(session.crm_context, request)
        system_message = SimulationMessage(
            role="system",
            content=result.execution.message,
            at=utc_now(),
            metadata={
                "action_id": result.execution.action_id,
                "execution_id": result.execution.execution_id,
            },
        )
        updated = session.model_copy(
            update={
                "crm_context": result.context,
                "crm_actions": [*session.crm_actions, result.execution],
                "messages": [*session.messages, system_message],
            }
        )
        self._session_store.save(updated)
        self._append_audit(
            "crm.action_executed",
            updated,
            {
                "action_id": result.execution.action_id,
                "execution_id": result.execution.execution_id,
                "status": result.execution.status,
                "output": result.execution.output,
            },
            context,
        )
        self._event_bus.publish(
            Event(
                event_type="crm.action_executed",
                tenant_id=session.tenant_id,
                payload={
                    "session_id": session.session_id,
                    "action_id": result.execution.action_id,
                    "execution_id": result.execution.execution_id,
                },
            )
        )
        return ExecuteCrmActionResponse(session_id=session_id, action=result.execution)

    def get_audit_trail(
        self,
        session_id: str,
        context: TenantContext | None = None,
    ) -> list[AuditRecord]:
        self.get_session(session_id, context)
        return self._audit_event_store.list_by_aggregate("simulation_session", session_id)

    def get_session_report(
        self,
        session_id: str,
        context: TenantContext | None = None,
    ) -> SessionReport:
        session = self.get_session(session_id, context)
        audit_records = self._audit_event_store.list_by_aggregate(
            "simulation_session",
            session_id,
        )
        report = self._evaluation_service.build_session_report(session, audit_records)
        # Enrich with procedural progress when the bridge is active
        if session.procedure_execution_id and self._conversation_service is not None:
            procedure_progress = self._fetch_procedure_progress(session.procedure_execution_id)
            report = report.model_copy(
                update={
                    "procedure_execution_id": session.procedure_execution_id,
                    "procedure_progress": procedure_progress,
                }
            )
        return report

    def _fetch_procedure_progress(self, execution_id: str) -> list[dict]:
        """Retrieve step results from the active procedure execution."""
        if self._conversation_service is None:
            return []
        try:
            proc_svc = self._conversation_service._procedure_service  # type: ignore[attr-defined]
            execution = proc_svc.get_execution(execution_id)
            return [
                {
                    "step_id": s.step_id,
                    "status": s.status,
                    "score": s.score,
                    "completed_at": s.completed_at.isoformat() if s.completed_at else None,
                }
                for s in execution.steps
            ]
        except Exception as exc:  # noqa: BLE001
            log.warning("simulation.bridge: could not fetch procedure progress (%s)", exc)
            return []

    def _append_audit(
        self,
        event_type: str,
        session: SimulationSession,
        payload: dict,
        context: TenantContext | None,
    ) -> None:
        trace_id = context.trace_id if context and context.trace_id else new_trace_id()
        actor_id = context.user_id if context and context.user_id else session.learner_id
        self._audit_event_store.append(
            AuditRecord(
                audit_id=new_id("audit"),
                event_type=event_type,
                tenant_id=session.tenant_id,
                aggregate_type="simulation_session",
                aggregate_id=session.session_id,
                occurred_at=utc_now(),
                trace_id=trace_id,
                actor_id=actor_id,
                payload=payload,
            )
        )

    @staticmethod
    def _count_messages(session: SimulationSession, role: str) -> int:
        return sum(1 for message in session.messages if message.role == role)

    @staticmethod
    def _customer_reply(
        scenario: ScenarioDefinition,
        learner_turn_count: int,
        evaluation: SimulationEvaluation,
    ) -> str:
        if any(
            criterion.criterion_id == "identity_verification" and criterion.status == "missed"
            for criterion in evaluation.criteria
        ):
            return "Avant d'aller plus loin, avez-vous besoin de mon numero de commande ?"
        if evaluation.score < 55:
            return "Je comprends, mais je ne suis pas encore rassure sur ce qui va etre fait."
        index = min(learner_turn_count - 1, len(scenario.customer_replies) - 1)
        return scenario.customer_replies[index]

    def _run_planning(
        self,
        session: SimulationSession,
        learner_turn_count: int,
        evaluation: SimulationEvaluation,
        learner_content: str,
    ) -> tuple[DirectorDecision | None, ResponsePlan | None]:
        """Run Director + Planner to decide the next stage and produce a plan."""
        try:
            stage_str = session.current_step
            stage = ConversationStage(stage_str) if stage_str else ConversationStage.opening
        except ValueError:
            stage = ConversationStage.opening

        director_ctx = DirectorContext(
            session_id=session.session_id,
            tenant_id=session.tenant_id,
            scenario_id=session.scenario.scenario_id,
            persona_id="",
            stage=stage,
            turn_count=learner_turn_count,
            learner_message_count=learner_turn_count,
            current_score=evaluation.score if evaluation else 0,
            last_learner_emotion="neutral",
        )
        decision = self._director.decide(director_ctx)

        planning_ctx = PlanningContext(
            scenario_id=session.scenario.scenario_id,
            persona_id="",
            procedure_id=session.scenario.scenario_id,
            procedure_step_id=decision.next_stage.value,
            current_stage=decision.next_stage.value,
            learner_message=learner_content,
            last_customer_message="",
            evaluation_score=evaluation.score if evaluation else 0,
            turn_count=learner_turn_count,
            crm_context=dict(session.crm_context),
        )
        plan = self._planner.plan(planning_ctx)
        return decision, plan

    def _validate_and_regenerate(
        self,
        session_id: str,
        message: str,
        response_plan: ResponsePlan,
        content: str,
        attempt: int,
    ) -> tuple[str, ValidationResult | None]:
        """Validate LLM output against the plan. If invalid, retry up to N times."""
        if response_plan is None:
            return content, None

        result = self._validator.validate(content, response_plan)
        if result.valid:
            return content, result

        log.warning(
            "validation: attempt %d failed — %d violations, score=%.2f, regenerate=%s",
            attempt + 1,
            len(result.violations),
            result.score,
            result.regenerate,
        )
        from callibr_telemetry import validation_results_total

        validation_results_total.labels(
            valid=str(result.valid),
            regenerate=str(result.regenerate),
            violation_codes="|".join(v.code for v in result.violations[:5]),
        ).inc()
        return content, result

    def _bridge_customer_reply(
        self,
        session: SimulationSession,
        scenario: ScenarioDefinition,
        learner_turn_count: int,
        evaluation: SimulationEvaluation,
        response_plan: ResponsePlan | None = None,
    ) -> str:
        """Generate the customer reply via ConversationService if bridge is active.

        Falls back to the static _customer_reply() when the bridge is inactive
        or if the ConversationService call fails.
        """
        if self._conversation_service is None or session.conversation_session_id is None:
            return self._customer_reply(scenario, learner_turn_count, evaluation)
        try:
            last_msg = self._last_learner_message(session)
            result = None
            validation_result: ValidationResult | None = None
            for attempt in range(self._validation_max_retries + 1):
                conv_result = self._conversation_service.process_message(
                    session_id=session.conversation_session_id,
                    message=last_msg if attempt == 0 else last_msg,
                    response_plan=response_plan,
                )
                content = conv_result.response.content
                if response_plan is not None:
                    content, validation_result = self._validate_and_regenerate(
                        session.session_id, last_msg, response_plan, content, attempt
                    )
                    if (
                        validation_result
                        and not validation_result.valid
                        and validation_result.regenerate
                        and attempt < self._validation_max_retries
                    ):
                        last_msg = content
                        continue
                result = content
                break

            return result or content
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "simulation.bridge: LLM reply failed (%s) — falling back to static reply",
                exc,
            )
            return self._customer_reply(scenario, learner_turn_count, evaluation)

    @staticmethod
    def _last_learner_message(session: SimulationSession) -> str:
        """Return the content of the most recent learner message."""
        for msg in reversed(session.messages):
            if msg.role == "learner":
                return msg.content
        return ""

    @staticmethod
    def _next_step(learner_turn_count: int, evaluation: SimulationEvaluation) -> str:
        if learner_turn_count >= 4 and evaluation.score >= 70:
            return "closing"
        if evaluation.score < 55:
            return "repair"
        return "resolution"

    @staticmethod
    def _assert_session_access(
        session: SimulationSession,
        context: TenantContext | None,
    ) -> None:
        if context is None:
            return
        if session.tenant_id != context.tenant_id:
            raise SimulationAccessForbiddenError(session.session_id, context.tenant_id)
