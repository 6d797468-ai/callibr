from __future__ import annotations

from callibr_api.main import create_app
from fastapi.testclient import TestClient


def test_list_scenarios() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/scenarios")

    assert response.status_code == 200
    assert response.json()[0]["scenario_id"] == "sav-retard-colis-001"


def test_start_simulation() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/simulations",
        json={
            "tenant_id": "tenant_demo",
            "learner_id": "learner_demo",
            "scenario_id": "sav-retard-colis-001",
        },
    )

    payload = response.json()
    assert response.status_code == 201
    assert payload["session_id"].startswith("sim_")
    assert payload["messages"][0]["role"] == "customer"


def test_start_simulation_uses_tenant_headers() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/simulations",
        headers={"X-Tenant-Id": "tenant_acme", "X-User-Id": "agent_007"},
        json={
            "tenant_id": "ignored_tenant",
            "learner_id": "ignored_user",
            "scenario_id": "sav-retard-colis-001",
        },
    )

    payload = response.json()
    assert response.status_code == 201
    assert payload["tenant_id"] == "tenant_acme"
    assert payload["learner_id"] == "agent_007"


def test_current_user_returns_demo_identity() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/v1/me",
        headers={
            "X-Tenant-Id": "tenant_acme",
            "X-User-Id": "agent_007",
            "X-Trace-Id": "trace_007",
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["tenant_id"] == "tenant_acme"
    assert payload["user_id"] == "agent_007"
    assert payload["trace_id"] == "trace_007"


def test_login_returns_bearer_token_and_me_accepts_it() -> None:
    client = TestClient(create_app())
    login_response = client.post(
        "/api/v1/auth/login",
        headers={"X-Trace-Id": "trace_login"},
        json={
            "tenant_id": "tenant_demo",
            "email": "learner@demo.callibr.local",
            "password": "callibr-demo",
        },
    )
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token}", "X-Trace-Id": "trace_me"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert me_response.status_code == 200
    assert me_response.json()["user_id"] == "learner_demo"
    assert me_response.json()["trace_id"] == "trace_me"


def test_login_rejects_invalid_password() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/auth/login",
        json={
            "tenant_id": "tenant_demo",
            "email": "learner@demo.callibr.local",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
    assert response.json()["code"] == "AUTHENTICATION_FAILED"


def test_start_simulation_accepts_bearer_token_context() -> None:
    client = TestClient(create_app())
    token = client.post(
        "/api/v1/auth/login",
        json={
            "tenant_id": "tenant_demo",
            "email": "learner@demo.callibr.local",
            "password": "callibr-demo",
        },
    ).json()["access_token"]

    response = client.post(
        "/api/v1/simulations",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_id": "sav-retard-colis-001"},
    )

    payload = response.json()
    assert response.status_code == 201
    assert payload["tenant_id"] == "tenant_demo"
    assert payload["learner_id"] == "learner_demo"


def test_send_simulation_message() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    response = client.post(
        f"/api/v1/simulations/{session_id}/messages",
        json={
            "content": (
                "Je comprends votre situation. Pouvez-vous confirmer le numero de commande ? "
                "Je vais verifier le suivi transporteur et vous proposer la prochaine etape."
            )
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["evaluation"]["score"] >= 70
    assert payload["session"]["messages"][-1]["role"] == "customer"


def test_unknown_scenario_returns_structured_error() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "unknown"},
    )

    assert response.status_code == 404
    assert response.json()["code"] == "SCENARIO_NOT_FOUND"


def test_list_crm_actions_for_session() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    response = client.get(f"/api/v1/simulations/{session_id}/crm/actions")

    action_ids = [action["action_id"] for action in response.json()]
    assert response.status_code == 200
    assert "verification_identite" in action_ids
    assert "creation_ticket_transporteur" in action_ids


def test_execute_crm_action_updates_session_state() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    action_response = client.post(
        f"/api/v1/simulations/{session_id}/crm/actions",
        json={"action_id": "verification_identite"},
    )
    session_response = client.get(f"/api/v1/simulations/{session_id}")

    assert action_response.status_code == 200
    assert action_response.json()["action"]["status"] == "succeeded"
    assert session_response.json()["crm_context"]["identity_verified"] is True


def test_blocked_crm_action_returns_conflict() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    response = client.post(
        f"/api/v1/simulations/{session_id}/crm/actions",
        json={"action_id": "creation_ticket_transporteur"},
    )

    assert response.status_code == 409
    assert response.json()["code"] == "CRM_ACTION_BLOCKED"


def test_simulation_audit_endpoint_returns_session_events() -> None:
    client = TestClient(create_app())
    headers = {
        "X-Tenant-Id": "tenant_acme",
        "X-User-Id": "agent_007",
        "X-Trace-Id": "trace_audit",
    }
    start_response = client.post(
        "/api/v1/simulations",
        headers=headers,
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    client.post(
        f"/api/v1/simulations/{session_id}/messages",
        headers=headers,
        json={"content": "Je vais verifier votre numero de commande."},
    )
    audit_response = client.get(
        f"/api/v1/simulations/{session_id}/audit",
        headers=headers,
    )

    events = audit_response.json()
    assert audit_response.status_code == 200
    assert [event["event_type"] for event in events] == [
        "simulation.started",
        "simulation.message_processed",
    ]
    assert events[0]["tenant_id"] == "tenant_acme"
    assert events[0]["trace_id"] == "trace_audit"


def test_simulation_report_endpoint_returns_detailed_scorecard() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    client.post(
        f"/api/v1/simulations/{session_id}/messages",
        json={
            "content": (
                "Je suis desole pour ce retard. Pouvez-vous confirmer votre numero de "
                "commande ? Je vais ouvrir un ticket transporteur, vous donner un delai "
                "de livraison et confirmer le suivi avec un recap."
            )
        },
    )
    report_response = client.get(f"/api/v1/simulations/{session_id}/report")

    payload = report_response.json()
    assert report_response.status_code == 200
    assert payload["session_id"] == session_id
    assert payload["final_score"] == 100
    assert len(payload["criteria"]) == 5
    assert {criterion["status"] for criterion in payload["criteria"]} == {"passed"}
    assert payload["message_count"] == 3
    assert payload["audit_event_count"] == 2


def test_cross_tenant_session_read_is_forbidden() -> None:
    client = TestClient(create_app())
    start_response = client.post(
        "/api/v1/simulations",
        headers={"X-Tenant-Id": "tenant_acme", "X-User-Id": "agent_007"},
        json={"scenario_id": "sav-retard-colis-001"},
    )
    session_id = start_response.json()["session_id"]

    response = client.get(
        f"/api/v1/simulations/{session_id}",
        headers={"X-Tenant-Id": "tenant_other", "X-User-Id": "agent_999"},
    )

    assert response.status_code == 403
    assert response.json()["code"] == "SIMULATION_ACCESS_FORBIDDEN"
