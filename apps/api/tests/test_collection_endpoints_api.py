from __future__ import annotations

from callibr_api.dependencies import get_session_store
from callibr_api.main import create_app
from callibr_api.routes.voice import _voice_service
from callibr_contracts.simulation import SimulationEvaluation
from fastapi.testclient import TestClient


def _scenario_payload() -> dict:
    return {
        "tenant_id": "tenant_demo",
        "learner_id": "learner_demo",
        "scenario_id": "sav-retard-colis-001",
    }


def _start_session(client: TestClient) -> str:
    response = client.post("/api/v1/simulations", json=_scenario_payload())
    assert response.status_code == 201
    return response.json()["session_id"]


def test_list_simulations_empty_on_fresh_app() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/simulations")

    assert response.status_code == 200
    assert response.json() == []


def test_list_simulations_shape_after_start() -> None:
    client = TestClient(create_app())
    session_id = _start_session(client)

    response = client.get("/api/v1/simulations")

    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    item = items[0]
    assert item["session_id"] == session_id
    assert set(item) == {
        "session_id",
        "scenario_id",
        "scenario_title",
        "domain_pack",
        "channel",
        "status",
        "started_at",
        "completed_at",
        "score",
        "max_score",
    }
    assert item["status"] == "active"
    assert item["scenario_title"]
    assert item["score"] is None


def test_list_reports_empty_without_completed_session() -> None:
    client = TestClient(create_app())
    _start_session(client)

    response = client.get("/api/v1/reports")

    assert response.status_code == 200
    assert response.json() == []


def test_list_reports_contains_completed_session() -> None:
    client = TestClient(create_app())
    session_id = _start_session(client)

    store = get_session_store()
    stored = store.get(session_id)
    assert stored is not None
    completed = stored.model_copy(
        update={
            "status": "completed",
            "evaluation": SimulationEvaluation(score=85),
        }
    )
    store.save(completed)

    response = client.get("/api/v1/reports")

    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["session_id"] == session_id
    assert items[0]["score"] == 85
    assert items[0]["max_score"] == 100
    assert items[0]["duration_minutes"] >= 0


def test_list_feedback_empty_then_contains_record() -> None:
    client = TestClient(create_app())
    session_id = _start_session(client)

    assert client.get("/api/v1/feedback").json() == []

    feedback = {
        "session_id": session_id,
        "tenant_id": "tenant_demo",
        "learner_id": "learner_demo",
        "satisfaction": 4,
        "perceived_realism": 4,
        "difficulty": 3,
        "usefulness": 5,
        "would_use_for_training": "yes",
        "free_text": "très utile",
    }
    submitted = client.post("/api/v1/feedback", json=feedback)
    assert submitted.status_code == 201

    response = client.get("/api/v1/feedback")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["session_id"] == session_id
    assert items[0]["satisfaction"] == 4
    assert items[0]["would_use_for_training"] == "yes"


def test_product_events_flow() -> None:
    client = TestClient(create_app())

    counts_before = client.get("/api/v1/product/events/counts").json()
    assert isinstance(counts_before, dict)
    seen_before = counts_before.get("ScenarioViewed", 0)

    client.post("/api/v1/product/events/ingest", json={"event_type": "ScenarioViewed"})
    client.post("/api/v1/product/events/ingest", json={"event_type": "ScenarioViewed"})

    counts_after = client.get("/api/v1/product/events/counts").json()
    assert counts_after.get("ScenarioViewed", 0) == seen_before + 2
    events = client.get("/api/v1/product/events").json()
    assert len(events) >= 2
    assert all(e["event_type"] for e in events)


def test_voice_sessions_list_and_create() -> None:
    client = TestClient(create_app())
    _voice_service.clear()

    assert client.get("/api/v1/voice/sessions").json() == []

    session_id = _start_session(client)
    created = client.post(
        "/api/v1/voice/sessions", params={"simulation_session_id": session_id}
    )
    assert created.status_code == 200
    voice_id = created.json()["session_id"]

    response = client.get("/api/v1/voice/sessions")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["session_id"] == voice_id
    assert items[0]["simulation_session_id"] == session_id
    assert items[0]["state"] == "idle"
