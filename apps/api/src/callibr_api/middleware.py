"""FastAPI middleware for observability."""

from __future__ import annotations

import time
from collections.abc import Callable

from callibr_telemetry import http_request_duration_seconds, http_requests_total
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        method = request.method

        # Extract the path template if available to avoid cardinalty explosion (e.g. /api/v1/sessions/123 -> /api/v1/sessions/{session_id})
        route = request.scope.get("route")
        endpoint = route.path if route else request.url.path

        # Ignore metrics endpoint to avoid recursive tracking
        if endpoint == "/metrics":
            return await call_next(request)

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
        except Exception:
            status_code = "500"
            raise
        finally:
            duration = time.perf_counter() - start_time
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
            http_requests_total.labels(
                method=method, endpoint=endpoint, status_code=status_code
            ).inc()

        return response
