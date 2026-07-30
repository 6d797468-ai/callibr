"""Tests unitaires et intégration pour l'observabilité (Sprint 16)."""

from __future__ import annotations

from callibr_api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_metrics_endpoint_returns_prometheus_format() -> None:
    # First, make a request to any endpoint to trigger the middleware
    client.get("/api/v1/scenarios", headers={"X-Tenant-ID": "tenant_demo"})

    # Then hit the metrics endpoint
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]

    content = response.text

    # Verify our custom metrics are present in the output
    assert "callibr_http_requests_total" in content
    assert "callibr_http_request_duration_seconds" in content
    assert "callibr_simulations_started_total" in content
    assert "callibr_llm_tokens_total" in content

    # Verify the specific request was recorded (200 OK on GET)
    assert 'method="GET"' in content
    assert 'status_code="200"' in content
