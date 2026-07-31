from __future__ import annotations

from typing import Any


class CallibrError(Exception):
    """Base application error with a stable machine-readable code."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
        title: str | None = None,
        explanation: str | None = None,
        action: str | None = None,
        retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
        self.title = title
        self.explanation = explanation
        self.action = action
        self.retryable = retryable


class HandlerAlreadyRegisteredError(CallibrError):
    def __init__(self, key: str) -> None:
        super().__init__(
            "HANDLER_ALREADY_REGISTERED",
            f"A handler is already registered for {key}.",
            details={"key": key},
        )


class HandlerNotFoundError(CallibrError):
    def __init__(self, key: str) -> None:
        super().__init__(
            "HANDLER_NOT_FOUND",
            f"No handler is registered for {key}.",
            details={"key": key},
        )
