from __future__ import annotations

import logging


class CallibrLogFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            "%(asctime)s %(levelname)s %(name)s trace_id=%(trace_id)s "
            "tenant_id=%(tenant_id)s %(message)s"
        )

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "trace_id"):
            record.trace_id = "-"
        if not hasattr(record, "tenant_id"):
            record.tenant_id = "-"
        return super().format(record)


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level)

    if any(getattr(handler, "callibr_managed", False) for handler in root.handlers):
        return

    handler = logging.StreamHandler()
    handler.setFormatter(CallibrLogFormatter())
    handler.callibr_managed = True
    root.addHandler(handler)


def bind_log_context(
    logger: logging.Logger,
    *,
    tenant_id: str | None = None,
    trace_id: str | None = None,
) -> logging.LoggerAdapter:
    return logging.LoggerAdapter(
        logger,
        {
            "tenant_id": tenant_id or "-",
            "trace_id": trace_id or "-",
        },
    )
