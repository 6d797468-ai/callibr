from __future__ import annotations

from callibr_contracts import ExecuteCrmActionRequest, SendMessageRequest, StartSimulationRequest
from callibr_crm import CrmActionService
from callibr_evaluation import EvaluationService
from callibr_kernel import EventBus, TenantContext
from callibr_persistence import InMemoryAuditEventStore, InMemorySimulationSessionStore
from callibr_scenario import InMemoryScenarioRepository
from callibr_simulation import SimulationService


def _make_service() -> SimulationService:
    return SimulationService(
        scenario_repository=InMemoryScenarioRepository(),
        crm_action_service=CrmActionService(),
        evaluation_service=EvaluationService(),
        session_store=InMemorySimulationSessionStore(),
        audit_event_store=InMemoryAuditEventStore(),
        event_bus=EventBus(),
    )


def test_simulation_service_starts_session_with_opening_message() -> None:
    service = _make_service()

    session = service.start_session(
        StartSimulationRequest(scenario_id="sav-retard-colis-001", tenant_id="tenant_demo")
    )

    assert session.session_id.startswith("sim_")
    assert session.scenario.scenario_id == "sav-retard-colis-001"
    assert session.messages[0].role == "customer"


def test_simulation_service_processes_learner_message() -> None:
    service = _make_service()
    session = service.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))

    response = service.send_message(
        session.session_id,
        SendMessageRequest(
            content=(
                "Je suis desole pour ce retard. Pouvez-vous me confirmer votre numero de "
                "commande ? Je vais verifier avec le transporteur et vous donner un delai."
            )
        ),
    )

    assert response.evaluation.score >= 70
    assert len(response.evaluation.criteria) == 5
    assert response.customer_message.role == "customer"
    assert response.session.current_step == "discovery"


def test_simulation_service_executes_crm_action_and_updates_session() -> None:
    service = _make_service()
    session = service.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))

    action_response = service.execute_crm_action(
        session.session_id,
        ExecuteCrmActionRequest(action_id="verification_identite"),
    )
    updated = service.get_session(session.session_id)

    assert action_response.action.action_id == "verification_identite"
    assert updated.crm_context["identity_verified"] is True
    assert updated.crm_actions[0].action_id == "verification_identite"
    assert updated.messages[-1].role == "system"


def test_simulation_service_appends_audit_records_with_context() -> None:
    service = _make_service()
    context = TenantContext(
        tenant_id="tenant_demo",
        user_id="agent_001",
        trace_id="trace_001",
    )
    session = service.start_session(
        StartSimulationRequest(scenario_id="sav-retard-colis-001", tenant_id="tenant_demo"),
        context,
    )

    service.send_message(
        session.session_id,
        SendMessageRequest(content="Je vais verifier votre numero de commande."),
        context,
    )

    audit_records = service.get_audit_trail(session.session_id)
    assert [record.event_type for record in audit_records] == [
        "simulation.started",
        "simulation.message_processed",
    ]
    assert {record.trace_id for record in audit_records} == {"trace_001"}
    assert {record.actor_id for record in audit_records} == {"agent_001"}


def test_simulation_service_generates_session_report() -> None:
    service = _make_service()
    session = service.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))

    service.send_message(
        session.session_id,
        SendMessageRequest(
            content=(
                "Je suis desole pour ce retard. Pouvez-vous me confirmer le numero de "
                "commande ? Je vais creer un ticket transporteur avec un delai et un recap."
            )
        ),
    )

    report = service.get_session_report(session.session_id)

    assert report.session_id == session.session_id
    assert report.final_score == 100
    assert len(report.criteria) == 5
    assert report.message_count == 3
    assert report.audit_event_count == 2
