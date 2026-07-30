from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, TypeVar

from callibr_kernel.errors import HandlerAlreadyRegisteredError, HandlerNotFoundError
from callibr_kernel.ids import new_id, new_trace_id
from callibr_kernel.time import utc_now

CommandT = TypeVar("CommandT", bound="Command")
ResultT = TypeVar("ResultT")


@dataclass(frozen=True, slots=True)
class Command:
    tenant_id: str
    command_id: str = field(default_factory=lambda: new_id("cmd"))
    trace_id: str = field(default_factory=new_trace_id)
    issued_at: datetime = field(default_factory=utc_now)


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[type[Command], Callable[[Any], Any]] = {}

    def register(
        self,
        command_type: type[CommandT],
        handler: Callable[[CommandT], ResultT],
    ) -> None:
        if command_type in self._handlers:
            raise HandlerAlreadyRegisteredError(command_type.__name__)
        self._handlers[command_type] = handler

    def dispatch(self, command: CommandT) -> Any:
        command_type = type(command)
        handler = self._handlers.get(command_type)
        if handler is None:
            raise HandlerNotFoundError(command_type.__name__)
        return handler(command)


class CommandHandler[CommandT: Command, ResultT](ABC):
    @abstractmethod
    def __call__(self, command: CommandT) -> ResultT: ...
