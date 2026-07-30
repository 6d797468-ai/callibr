"""Tests unitaires — S13 Bridge SimulationService ↔ ConversationService.

Couvre :
- Bridge désactivé : comportement original inchangé (conversation_session_id=None)
- Bridge activé  : conversation_session_id présent dans la session démarrée
- Bridge activé  : réponse client générée via ConversationService.process_message()
- Bridge fallback : si ConversationService lève une exception, retour aux réponses statiques
- SessionReport  : procedure_progress enrichi quand bridge est actif
- Mapping SCENARIO_BRIDGE_MAP : couverture des deux scénarios G1-SUPPORT-SAV
"""

from __future__ import annotations

from unittest.mock import MagicMock
from uuid import uuid4

from callibr_contracts import (
    ConversationContext,
    ConversationResult,
    ConversationState,
    ModelResponse,
    SendMessageRequest,
    StartSimulationRequest,
)
from callibr_kernel import EventBus, utc_now
from callibr_persistence import (
    InMemoryAuditEventStore,
    InMemorySimulationSessionStore,
)
from callibr_simulation.service import SCENARIO_BRIDGE_MAP, SimulationService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_scenario_repository(scenario_id: str = "sav-retard-colis-001"):
    """Return a minimal ScenarioRepository mock for the simulation engine."""
    from callibr_contracts import ScenarioSummary

    summary = ScenarioSummary(
        scenario_id=scenario_id,
        domain_pack="G1-SUPPORT-SAV",
        title="SAV Test",
        level="foundation",
        channel="chat",
        estimated_minutes=8,
        learning_goals=["empathie"],
    )

    mock_scenario = MagicMock()
    mock_scenario.summary = summary
    mock_scenario.opening_message = "Bonjour, j'ai un problème avec ma commande."
    mock_scenario.crm_context = {"scenario_id": scenario_id}
    mock_scenario.customer_replies = [
        "D'accord, merci.",
        "Je comprends, j'attends votre retour.",
        "Parfait, merci beaucoup.",
    ]

    repo = MagicMock()
    repo.list_scenarios.return_value = [summary]
    repo.get.return_value = mock_scenario
    return repo


def _make_service(
    scenario_id: str = "sav-retard-colis-001",
    conversation_service=None,
) -> SimulationService:
    from callibr_crm import CrmActionService
    from callibr_evaluation import EvaluationService

    return SimulationService(
        scenario_repository=_make_mock_scenario_repository(scenario_id),
        crm_action_service=CrmActionService(),
        evaluation_service=EvaluationService(),
        session_store=InMemorySimulationSessionStore(),
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
        conversation_service=conversation_service,
    )


def _make_mock_conversation_result(session_id: str = "conv_test_001") -> ConversationResult:
    """Build a minimal ConversationResult as returned by ConversationService."""
    from callibr_contracts import ConversationMetadata

    return ConversationResult(
        context=ConversationContext(
            metadata=ConversationMetadata(
                execution_id="proc-exec_test_abc",
                procedure_id="proc-sav-retard-colis-001",
                persona_id="persona-sav-client-frustre-001",
                scenario_id="sc-sav-retard-colis-v1",
            ),
        ),
        response=ModelResponse(
            content="Ceci est une réponse LLM simulée.",
            model_id="mock",
        ),
        state=ConversationState(
            session_id=session_id,
            correlation_id=uuid4(),
            turns=[],
            started_at=utc_now(),
            updated_at=utc_now(),
        ),
    )


# ---------------------------------------------------------------------------
# SCENARIO_BRIDGE_MAP
# ---------------------------------------------------------------------------


class TestScenarioBridgeMap:
    def test_both_sav_scenarios_are_mapped(self) -> None:
        assert "sav-retard-colis-001" in SCENARIO_BRIDGE_MAP
        assert "sav-erreur-facturation-001" in SCENARIO_BRIDGE_MAP

    def test_mapped_ids_point_to_engine_scenarios(self) -> None:
        assert SCENARIO_BRIDGE_MAP["sav-retard-colis-001"] == "sc-sav-retard-colis-v1"
        assert SCENARIO_BRIDGE_MAP["sav-erreur-facturation-001"] == "sc-sav-erreur-facturation-v1"

    def test_unknown_scenario_not_in_map(self) -> None:
        assert "some-custom-scenario-999" not in SCENARIO_BRIDGE_MAP


# ---------------------------------------------------------------------------
# Bridge désactivé (conversation_service=None)
# ---------------------------------------------------------------------------


class TestBridgeDisabled:
    def test_start_session_without_bridge_has_no_conversation_ids(self) -> None:
        svc = _make_service(conversation_service=None)
        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        assert session.conversation_session_id is None
        assert session.procedure_execution_id is None

    def test_send_message_without_bridge_uses_static_reply(self) -> None:
        svc = _make_service(conversation_service=None)
        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        response = svc.send_message(
            session.session_id,
            SendMessageRequest(
                content="Bonjour, je suis désolé pour ce retard. Votre numéro de commande ?"
            ),
        )
        # Static replies come from scenario.customer_replies
        assert len(response.customer_message.content) > 0
        assert response.customer_message.metadata.get("bridge") is False

    def test_get_session_report_without_bridge_has_no_procedure_progress(self) -> None:
        svc = _make_service(conversation_service=None)
        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        report = svc.get_session_report(session.session_id)
        assert report.procedure_progress == []
        assert report.procedure_execution_id is None


# ---------------------------------------------------------------------------
# Bridge activé
# ---------------------------------------------------------------------------


class TestBridgeEnabled:
    def _make_conv_svc_mock(
        self,
        conv_session_id: str = "conv_bridge_001",
        fail_start: bool = False,
        fail_process: bool = False,
    ):
        mock_svc = MagicMock()

        if fail_start:
            mock_svc.start_conversation.side_effect = RuntimeError("LLM unavailable")
        else:
            mock_svc.start_conversation.return_value = _make_mock_conversation_result(
                conv_session_id
            )

        if fail_process:
            mock_svc.process_message.side_effect = RuntimeError("LLM timeout")
        else:
            mock_svc.process_message.return_value = ConversationResult(
                context=ConversationContext(),
                response=ModelResponse(content="Réponse LLM bridge.", model_id="mock"),
                state=ConversationState(
                    session_id=conv_session_id,
                    correlation_id=uuid4(),
                    turns=[],
                    started_at=utc_now(),
                    updated_at=utc_now(),
                ),
            )

        # Procedure progress fetch
        proc_execution = MagicMock()
        proc_execution.steps = [
            MagicMock(step_id="s1", status="completed", score=90, completed_at=utc_now()),
            MagicMock(step_id="s2", status="active", score=0, completed_at=None),
        ]
        mock_svc._procedure_service = MagicMock()
        mock_svc._procedure_service.get_execution.return_value = proc_execution

        return mock_svc

    def test_start_session_populates_conversation_session_id(self) -> None:
        conv_svc = self._make_conv_svc_mock("conv_bridge_abc")
        svc = _make_service(conversation_service=conv_svc)

        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))

        assert session.conversation_session_id == "conv_bridge_abc"
        assert session.procedure_execution_id == "proc-exec_test_abc"
        conv_svc.start_conversation.assert_called_once_with(
            scenario_id="sc-sav-retard-colis-v1",
            tenant_id="tenant_demo",
            actor_id="learner_demo",
        )

    def test_send_message_uses_llm_reply_when_bridge_active(self) -> None:
        conv_svc = self._make_conv_svc_mock()
        svc = _make_service(conversation_service=conv_svc)

        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        response = svc.send_message(
            session.session_id,
            SendMessageRequest(content="Votre numéro de commande s'il vous plaît ?"),
        )

        assert response.customer_message.content == "Réponse LLM bridge."
        assert response.customer_message.metadata.get("bridge") is True

    def test_session_report_includes_procedure_progress(self) -> None:
        conv_svc = self._make_conv_svc_mock()
        svc = _make_service(conversation_service=conv_svc)

        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        report = svc.get_session_report(session.session_id)

        assert report.procedure_execution_id == "proc-exec_test_abc"
        assert len(report.procedure_progress) == 2
        assert report.procedure_progress[0]["step_id"] == "s1"
        assert report.procedure_progress[0]["status"] == "completed"
        assert report.procedure_progress[1]["step_id"] == "s2"
        assert report.procedure_progress[1]["status"] == "active"

    def test_bridge_start_failure_falls_back_gracefully(self) -> None:
        """If ConversationService.start_conversation() fails, bridge is skipped."""
        conv_svc = self._make_conv_svc_mock(fail_start=True)
        svc = _make_service(conversation_service=conv_svc)

        # Must not raise — falls back silently
        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        assert session.conversation_session_id is None

    def test_bridge_message_failure_falls_back_to_static(self) -> None:
        """If process_message() fails, static reply is used as fallback."""
        conv_svc = self._make_conv_svc_mock(fail_process=True)
        svc = _make_service(conversation_service=conv_svc)

        session = svc.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
        # Bridge is active (start succeeded)
        assert session.conversation_session_id is not None

        response = svc.send_message(
            session.session_id,
            SendMessageRequest(content="Bonjour, je suis désolé."),
        )
        # Fallback to static reply — content is non-empty and does not crash
        assert len(response.customer_message.content) > 0

    def test_erreur_facturation_scenario_also_bridged(self) -> None:
        conv_svc = self._make_conv_svc_mock("conv_facturation_001")
        repo = _make_mock_scenario_repository("sav-erreur-facturation-001")
        from callibr_crm import CrmActionService
        from callibr_evaluation import EvaluationService

        svc = SimulationService(
            scenario_repository=repo,
            crm_action_service=CrmActionService(),
            evaluation_service=EvaluationService(),
            session_store=InMemorySimulationSessionStore(),
            audit_event_store=InMemoryAuditEventStore(),
            event_bus=EventBus(),
            conversation_service=conv_svc,
        )

        session = svc.start_session(
            StartSimulationRequest(scenario_id="sav-erreur-facturation-001")
        )

        assert session.conversation_session_id == "conv_facturation_001"
        conv_svc.start_conversation.assert_called_once_with(
            scenario_id="sc-sav-erreur-facturation-v1",
            tenant_id="tenant_demo",
            actor_id="learner_demo",
        )
