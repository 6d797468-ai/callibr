from __future__ import annotations

import psycopg
from callibr_api.main import create_app
from callibr_kernel import CallibrError
from fastapi.testclient import TestClient


def _error_fields(body: dict) -> None:
    for field in (
        "code",
        "message",
        "title",
        "explanation",
        "action",
        "retryable",
        "details",
        "http_status",
        "trace_id",
    ):
        assert field in body, f"missing error field {field}"


def test_scenario_not_found_error_shape() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "scenario-inexistant"},
    )

    body = response.json()
    assert response.status_code == 404
    assert body["code"] == "SCENARIO_NOT_FOUND"
    assert body["http_status"] == 404
    assert body["retryable"] is False
    _error_fields(body)


def test_validation_error_shape() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/simulations", json={"foo": "bar"})

    body = response.json()
    assert response.status_code == 422
    assert body["code"] == "VALIDATION_ERROR"
    assert body["title"] == "Requête invalide"
    assert body["retryable"] is True
    _error_fields(body)


def test_unhandled_exception_returns_structured_500() -> None:
    app = create_app()

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("kaboom")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/boom")

    body = response.json()
    assert response.status_code == 500
    assert body["code"] == "INTERNAL_ERROR"
    assert body["title"] == "Une erreur inattendue est survenue"
    assert body["retryable"] is True
    _error_fields(body)


def test_datastore_unavailable_is_503() -> None:
    app = create_app()

    @app.get("/db-down")
    def db_down() -> None:
        raise psycopg.OperationalError("connection refused")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/db-down")

    body = response.json()
    assert response.status_code == 503
    assert body["code"] == "DATASTORE_UNAVAILABLE"
    assert body["retryable"] is True
    _error_fields(body)


def test_llm_error_maps_to_503_with_friendly_fields() -> None:
    app = create_app()

    @app.get("/llm-down")
    def llm_down() -> None:
        raise CallibrError(
            "llm_error",
            "provider unavailable",
            title="Service d'IA indisponible",
            explanation="Le service d'intelligence artificielle est indisponible.",
            action="Réessayez dans quelques instants.",
            retryable=True,
        )

    client = TestClient(app)
    response = client.get("/llm-down")

    body = response.json()
    assert response.status_code == 503
    assert body["code"] == "llm_error"
    assert body["title"] == "Service d'IA indisponible"
    assert body["retryable"] is True
    _error_fields(body)


def test_voice_session_not_found_is_404() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/voice/sessions/unknown-session")

    body = response.json()
    assert response.status_code == 404
    assert body["code"] == "VOICE_SESSION_NOT_FOUND"
    _error_fields(body)


def test_voice_end_invalid_state_is_400() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/voice/sessions/unknown-session/end")

    body = response.json()
    assert response.status_code == 400
    assert body["code"] == "VOICE_SESSION_INVALID_STATE"
    _error_fields(body)


def test_error_body_carries_trace_id() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/simulations",
        json={"scenario_id": "scenario-inexistant"},
        headers={"X-Trace-Id": "trace_error_test"},
    )

    body = response.json()
    assert body["trace_id"] == "trace_error_test"
