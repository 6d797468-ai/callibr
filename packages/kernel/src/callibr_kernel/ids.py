from __future__ import annotations

from uuid import uuid4


def new_id(prefix: str) -> str:
    normalized = prefix.strip().lower().replace("_", "-")
    return f"{normalized}_{uuid4().hex}"


def new_trace_id() -> str:
    return new_id("trace")
