from __future__ import annotations

from callibr_contracts import AuditRecord, IdentityUserRecord, StartSimulationRequest, TenantInfo
from callibr_crm import CrmActionService
from callibr_evaluation import EvaluationService
from callibr_kernel import EventBus, utc_now
from callibr_persistence import (
    InMemoryAuditEventStore,
    InMemoryIdentityStore,
    InMemorySimulationSessionStore,
)
from callibr_persistence.postgres import normalize_psycopg_url
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


def test_in_memory_session_store_saves_and_loads_session() -> None:
    service = _make_service()
    session = service.start_session(StartSimulationRequest(scenario_id="sav-retard-colis-001"))
    store = InMemorySimulationSessionStore()

    store.save(session)

    loaded = store.get(session.session_id)
    assert loaded is not None
    assert loaded.session_id == session.session_id
    assert loaded.scenario.scenario_id == "sav-retard-colis-001"


def test_in_memory_audit_store_lists_by_aggregate() -> None:
    store = InMemoryAuditEventStore()
    record = AuditRecord(
        audit_id="audit_001",
        event_type="simulation.started",
        tenant_id="tenant_demo",
        aggregate_type="simulation_session",
        aggregate_id="sim_001",
        occurred_at=utc_now(),
        trace_id="trace_001",
        actor_id="learner_demo",
        payload={"scenario_id": "sav-retard-colis-001"},
    )

    store.append(record)

    assert store.list_by_aggregate("simulation_session", "sim_001") == [record]
    assert store.list_by_aggregate("simulation_session", "sim_002") == []


def test_normalize_psycopg_url_accepts_sqlalchemy_style_url() -> None:
    assert (
        normalize_psycopg_url("postgresql+psycopg://callibr:callibr@localhost:5432/callibr")
        == "postgresql://callibr:callibr@localhost:5432/callibr"
    )


def test_in_memory_identity_store_saves_tenant_and_user() -> None:
    store = InMemoryIdentityStore()
    tenant = TenantInfo(tenant_id="tenant_demo", name="Demo", environment="local")
    user = IdentityUserRecord(
        tenant_id="tenant_demo",
        user_id="learner_demo",
        email="learner@demo.callibr.local",
        display_name="Learner Demo",
        roles=["agent"],
        password_hash="hash",
    )

    store.save_tenant(tenant)
    store.save_user(user)

    assert store.get_tenant("tenant_demo") == tenant
    assert store.get_user("tenant_demo", "learner_demo") == user
    assert store.get_user_by_email("tenant_demo", "LEARNER@demo.callibr.local") == user
