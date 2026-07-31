from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

import pytest
from callibr_contracts.conversation import ConversationState, ConversationStore


class AbstractConversationStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> ConversationStore:
        pass

    def _make_state(self, session_id: str = "conv1") -> ConversationState:
        return ConversationState(
            session_id=session_id,
            correlation_id=uuid4(),
            version=1,
            started_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def test_save_and_get(self, store: ConversationStore):
        state = self._make_state()
        store.save(state)
        retrieved = store.get("conv1")
        assert retrieved is not None
        assert retrieved.session_id == "conv1"
        assert retrieved.version == 1

    def test_get_nonexistent(self, store: ConversationStore):
        assert store.get("nonexistent") is None

    def test_update(self, store: ConversationStore):
        state = self._make_state("s1")
        store.save(state)
        state2 = ConversationState(
            session_id="s1",
            correlation_id=uuid4(),
            version=2,
            started_at=datetime.now(),
            updated_at=datetime.now(),
        )
        store.save(state2)
        retrieved = store.get("s1")
        assert retrieved is not None
        assert retrieved.version == 2
