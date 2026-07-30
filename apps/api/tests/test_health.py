from __future__ import annotations

from callibr_api.main import create_app
from fastapi.testclient import TestClient


def test_health() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_platform_info() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/platform/info")

    assert response.status_code == 200
    assert response.json()["product"] == "Callibr"


def test_trace_header_is_returned() -> None:
    client = TestClient(create_app())

    response = client.get("/health", headers={"X-Trace-Id": "trace_test"})

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == "trace_test"
