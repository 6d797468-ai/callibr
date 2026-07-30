from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Protocol


class TransactionManager(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[Any]: ...
