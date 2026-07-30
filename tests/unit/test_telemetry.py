from __future__ import annotations

import logging
from io import StringIO

from callibr_telemetry import CallibrLogFormatter, bind_log_context


def test_log_formatter_includes_trace_and_tenant_context() -> None:
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(CallibrLogFormatter())

    logger = logging.getLogger("callibr.test.telemetry")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel("INFO")

    contextual_logger = bind_log_context(
        logger,
        tenant_id="tenant_demo",
        trace_id="trace_demo",
    )
    contextual_logger.info("simulation started")

    output = stream.getvalue()
    assert "trace_id=trace_demo" in output
    assert "tenant_id=tenant_demo" in output
    assert "simulation started" in output
