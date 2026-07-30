"""Turn and session memory for the Conversation Runtime."""

from __future__ import annotations

from typing import Any

from callibr_contracts import ConversationState, ConversationTurn
from callibr_kernel import new_id, utc_now


class TurnMemory:
    def __init__(self) -> None:
        self._turns: list[ConversationTurn] = []

    def add_turn(
        self, role: str, content: str, metadata: dict[str, Any] | None = None
    ) -> ConversationTurn:
        turn = ConversationTurn(
            turn_id=new_id("turn"),
            role=role,
            content=content,
            timestamp=utc_now(),
            metadata=metadata or {},
        )
        self._turns.append(turn)
        return turn

    def get_turns(self) -> list[ConversationTurn]:
        return list(self._turns)

    def last_turn(self) -> ConversationTurn | None:
        return self._turns[-1] if self._turns else None

    def clear(self) -> None:
        self._turns.clear()


class SessionMemory:
    def __init__(
        self, session_id: str, correlation_id: str | None = None, version: int = 0
    ) -> None:
        from uuid import uuid4

        self._session_id = session_id
        self._correlation_id = correlation_id or uuid4()
        self._version = version
        self._turn_memory = TurnMemory()
        self._variables: dict[str, Any] = {}
        self._started_at = utc_now()
        self._updated_at = utc_now()

    @property
    def session_id(self) -> str:
        return self._session_id

    def increment_version(self) -> int:
        self._version += 1
        return self._version

    @property
    def correlation_id(self) -> str:
        return self._correlation_id

    @classmethod
    def from_state(cls, state: ConversationState) -> SessionMemory:
        memory = cls(state.session_id, state.correlation_id, state.version)
        memory._started_at = state.started_at
        memory._updated_at = state.updated_at
        memory._variables = dict(state.variables)
        for turn in state.turns:
            memory._turn_memory._turns.append(turn)
        return memory

    def add_turn(
        self, role: str, content: str, metadata: dict[str, Any] | None = None
    ) -> ConversationTurn:
        self._updated_at = utc_now()
        return self._turn_memory.add_turn(role, content, metadata)

    def get_turns(self) -> list[ConversationTurn]:
        return self._turn_memory.get_turns()

    def last_turn(self) -> ConversationTurn | None:
        return self._turn_memory.last_turn()

    def set_variable(self, key: str, value: Any) -> None:
        self._variables[key] = value

    def get_variable(self, key: str) -> Any | None:
        return self._variables.get(key)

    def to_state(self) -> ConversationState:
        return ConversationState(
            session_id=self._session_id,
            correlation_id=self._correlation_id,
            version=self._version,
            turns=self.get_turns(),
            current_step_id=self._variables.get("current_step_id", ""),
            variables=dict(self._variables),
            started_at=self._started_at,
            updated_at=self._updated_at,
        )
