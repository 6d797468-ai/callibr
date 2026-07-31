from __future__ import annotations

from datetime import UTC, datetime, timedelta

from callibr_contracts import SimulationEvaluation, SimulationSession
from callibr_contracts.simulation import ScenarioSummary
from callibr_contracts.telemetry import FeedbackRecord, ProductEvent
from callibr_persistence.memory.feedback_store import MemoryFeedbackStore
from callibr_persistence.memory.product_event_store import MemoryProductEventStore
from callibr_persistence.session_store import InMemorySimulationSessionStore
from callibr_telemetry.pilot import PilotDashboardService


def _scenario() -> ScenarioSummary:
    return ScenarioSummary(
        scenario_id="sav-retard-colis-001",
        domain_pack="retail",
        title="Réclamation retard de colis",
        level="foundation",
        channel="chat",
        estimated_minutes=10,
    )


def _session(
    session_id: str,
    status: str = "completed",
    score: int = 85,
    duration_minutes: float = 12.0,
    learner_id: str = "learner_demo",
) -> SimulationSession:
    started = datetime.now(UTC)
    return SimulationSession(
        session_id=session_id,
        tenant_id="tenant_demo",
        learner_id=learner_id,
        scenario=_scenario(),
        status=status,
        current_step="done",
        started_at=started,
        completed_at=started + timedelta(minutes=duration_minutes) if status == "completed" else None,
        evaluation=SimulationEvaluation(score=score) if status == "completed" else None,
    )


def _event(event_type: str, session_id: str = "", timestamp: str = "") -> ProductEvent:
    return ProductEvent(
        event_type=event_type,
        tenant_id="tenant_demo",
        timestamp=timestamp or datetime.now(UTC).isoformat(),
        scenario_id="",
        persona_id="",
        procedure_id="",
        session_id=session_id,
        duration=0.0,
        version="0.1.0",
        metadata=None,
    )


def _service():
    return PilotDashboardService(
        session_store=InMemorySimulationSessionStore(),
        feedback_store=MemoryFeedbackStore(),
        product_event_store=MemoryProductEventStore(),
    )


def test_empty_dashboard_has_zero_kpis_and_info_alert() -> None:
    dashboard = _service().compute()

    assert dashboard.overview.simulations_total == 0
    assert dashboard.overview.success_rate == 0.0
    assert dashboard.overview.average_satisfaction == 0.0
    assert dashboard.overview.average_duration_minutes == 0.0
    assert [stage.count for stage in dashboard.funnel] == [0] * 6
    assert all(stage.percentage == 0.0 for stage in dashboard.funnel)
    assert dashboard.alerts[0].level == "info"
    assert dashboard.alerts[0].title == "Premières données attendues"


def test_funnel_percentages_relative_to_first_stage() -> None:
    service = _service()
    for event_type in ["ApplicationOpened", "WizardCompleted", "ScenarioStarted", "ConversationCompleted"]:
        service._product_event_store.record(_event(event_type))

    dashboard = service.compute()
    counts = [stage.count for stage in dashboard.funnel]

    assert counts == [1, 1, 1, 1, 0, 0]
    assert [stage.percentage for stage in dashboard.funnel][:4] == [100.0, 100.0, 100.0, 100.0]
    assert dashboard.funnel[4].percentage == 0.0
    assert [stage.label for stage in dashboard.funnel] == [
        "Premier lancement",
        "Wizard terminé",
        "Simulation lancée",
        "Simulation terminée",
        "Rapport consulté",
        "Feedback envoyé",
    ]


def test_overview_from_sessions_and_feedback() -> None:
    service = _service()
    store = service._session_store
    store.save(_session("sim_1", score=90, duration_minutes=10))
    store.save(_session("sim_2", score=50, duration_minutes=20))
    store.save(_session("sim_3", status="active"))
    service._feedback_store.submit(
        FeedbackRecord(
            session_id="sim_1",
            tenant_id="tenant_demo",
            learner_id="learner_demo",
            satisfaction=4,
            perceived_realism=4,
            difficulty=3,
            usefulness=4,
            would_use_for_training="yes",
            free_text="ok",
            submitted_at=datetime.now(UTC).isoformat(),
        )
    )

    dashboard = service.compute()

    assert dashboard.overview.simulations_total == 3
    assert dashboard.overview.success_rate == 33.3  # 1 of 3 above 70
    assert dashboard.overview.average_satisfaction == 4.0
    assert dashboard.overview.average_duration_minutes == 15.0


def test_alerts_on_abandons_duration_and_satisfaction() -> None:
    service = _service()
    store = service._session_store
    store.save(_session("sim_1", duration_minutes=20))
    service._product_event_store.record(_event("ScenarioStarted", "sim_1"))
    service._feedback_store.submit(
        FeedbackRecord(
            session_id="sim_1",
            tenant_id="tenant_demo",
            learner_id="learner_demo",
            satisfaction=3,
            perceived_realism=3,
            difficulty=3,
            usefulness=3,
            would_use_for_training="no",
            free_text="trop long",
            submitted_at=datetime.now(UTC).isoformat(),
        )
    )

    dashboard = service.compute()

    titles = [alert.title for alert in dashboard.alerts]
    assert "1 simulation abandonnée" in titles
    assert "Durée moyenne supérieure à 15 min" in titles
    assert "Satisfaction sous la cible (4/5)" in titles
    assert all(alert.level == "warning" for alert in dashboard.alerts)


def test_healthy_dashboard_reports_info_alert() -> None:
    service = _service()
    store = service._session_store
    store.save(_session("sim_1", score=85, duration_minutes=10))
    service._product_event_store.record(_event("ScenarioStarted", "sim_1"))
    service._product_event_store.record(_event("ConversationCompleted", "sim_1"))

    dashboard = service.compute()

    assert len(dashboard.alerts) == 1
    assert dashboard.alerts[0].level == "info"
    assert dashboard.alerts[0].title == "Système sain"


def test_recent_activity_is_chronological_and_resolves_actors() -> None:
    service = _service()
    store = service._session_store
    store.save(_session("sim_1", score=80))
    service._product_event_store.record(
        _event("ConversationCompleted", "sim_1", timestamp="2026-07-31T10:00:00+00:00")
    )
    service._product_event_store.record(
        _event("ScenarioStarted", "sim_1", timestamp="2026-07-31T09:00:00+00:00")
    )
    service._product_event_store.record(
        _event("FeedbackSubmitted", "sim_1", timestamp="2026-07-31T08:30:00+00:00")
    )
    service._feedback_store.submit(
        FeedbackRecord(
            session_id="sim_1",
            tenant_id="tenant_demo",
            learner_id="learner_demo",
            satisfaction=4,
            perceived_realism=4,
            difficulty=3,
            usefulness=4,
            would_use_for_training="yes",
            free_text="bien",
            submitted_at="2026-07-31T08:00:00+00:00",
        )
    )

    dashboard = service.compute()

    actions = [item.action for item in dashboard.recent_activity]
    assert actions == ["Simulation terminée", "Simulation lancée", "Feedback envoyé"]
    assert dashboard.recent_activity[0].detail == "Score 80/100"
    assert all(item.actor == "learner_demo" for item in dashboard.recent_activity)
    assert dashboard.recent_activity[2].detail == "★★★★"
