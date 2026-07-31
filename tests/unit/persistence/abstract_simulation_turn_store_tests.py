import pytest
from abc import ABC, abstractmethod
from callibr_contracts.ports import SimulationTurnStore
from callibr_contracts.simulation import SimulationMessage
from datetime import datetime

class AbstractSimulationTurnStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> SimulationTurnStore:
        pass

    def test_save_and_get_turns(self, store: SimulationTurnStore):
        session_id = "s1"
        turns = [
            SimulationMessage(role="learner", content="hello", at=datetime.now()),
            SimulationMessage(role="customer", content="hi", at=datetime.now()),
        ]
        store.save_turns(session_id, turns)
        
        saved_turns = store.get_turns(session_id)
        assert len(saved_turns) == 2
        assert saved_turns[0].content == "hello"
        assert saved_turns[1].content == "hi"

    def test_get_turns_nonexistent_session(self, store: SimulationTurnStore):
        assert store.get_turns("nonexistent") == []
