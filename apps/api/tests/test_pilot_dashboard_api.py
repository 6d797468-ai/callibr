from __future__ import annotations

import json

from callibr_api.main import create_app
from fastapi.testclient import TestClient


def _scenario_payload() -> dict:
    return {
        "tenant_id": "tenant_demo",
        "learner_id": "learner_demo",
        "scenario_id": "sav-retard-colis-001",
    }


def _feedback_payload(session_id: str) -> dict:
    return {
        "session_id": session_id,
        "tenant_id": "tenant_demo",
        "learner_id": "learner_demo",
        "satisfaction": 4,
        "perceived_realism": 4,
        "difficulty": 3,
        "usefulness": 4,
        "would_use_for_training": "yes",
        "free_text": "bonne simulation",
    }


def test_pilot_dashboard_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/pilot/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {"overview", "funnel", "recent_activity", "alerts"}
    assert set(payload["overview"]) == {
        "simulations_total",
        "success_rate",
        "average_satisfaction",
        "average_duration_minutes",
    }
    assert len(payload["funnel"]) == 6
    assert all(set(stage) == {"id", "label", "count", "percentage"} for stage in payload["funnel"])
    assert isinstance(payload["recent_activity"], list)
    assert isinstance(payload["alerts"], list)


def test_pilot_dashboard_has_no_technical_metrics() -> None:
    client = TestClient(create_app())

    payload = client.get("/api/v1/pilot/dashboard").json()
    blob = json.dumps(payload).lower()

    for term in ("tokens", "provider", "latency", "budget", "conversations", "prompt", "models"):
        assert term not in blob


def test_pilot_dashboard_reflects_simulation_and_feedback() -> None:
    client = TestClient(create_app())
    before = client.get("/api/v1/pilot/dashboard").json()

    simulation = client.post("/api/v1/simulations", json=_scenario_payload())
    assert simulation.status_code == 201
    session_id = simulation.json()["session_id"]

    feedback = client.post("/api/v1/feedback", json=_feedback_payload(session_id))
    assert feedback.status_code == 201

    after = client.get("/api/v1/pilot/dashboard").json()

    funnel_before = {stage["id"]: stage["count"] for stage in before["funnel"]}
    funnel_after = {stage["id"]: stage["count"] for stage in after["funnel"]}
    assert funnel_after["simulation_lancee"] == funnel_before["simulation_lancee"] + 1
    assert funnel_after["feedback_envoye"] == funnel_before["feedback_envoye"] + 1
    assert after["overview"]["simulations_total"] == before["overview"]["simulations_total"] + 1


def test_pilot_dashboard_recent_activity_shows_feedback() -> None:
    client = TestClient(create_app())

    simulation = client.post("/api/v1/simulations", json=_scenario_payload())
    session_id = simulation.json()["session_id"]
    client.post("/api/v1/feedback", json=_feedback_payload(session_id))

    payload = client.get("/api/v1/pilot/dashboard").json()

    actions = [item["action"] for item in payload["recent_activity"]]
    assert "Feedback envoyé" in actions
