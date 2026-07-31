import pytest
from abc import ABC, abstractmethod
from datetime import datetime
from callibr_contracts import SimulationSession
from callibr_contracts.simulation import ScenarioSummary
from callibr_contracts.ports import SimulationSessionStore

class AbstractSimulationSessionStoreTests(ABC):
    @pytest.fixture
    @abstractmethod
    def store(self) -> SimulationSessionStore:
        pass

    def _make_session(self, session_id: str = "s1") -> SimulationSession:
        return SimulationSession(
            session_id=session_id,
            tenant_id="t1",
            learner_id="l1",
            scenario=ScenarioSummary(
                scenario_id="sc1",
                domain_pack="retail",
                title="Test Scenario",
                level="foundation",
                channel="chat",
                estimated_minutes=10,
            ),
            status="active",
            current_step="intro",
            started_at=datetime.now(),
        )

    def test_save_and_get(self, store: SimulationSessionStore):
        session = self._make_session()
        store.save(session)
        retrieved = store.get("s1")
        assert retrieved is not None
        assert retrieved.session_id == "s1"
        assert retrieved.tenant_id == "t1"

    def test_get_nonexistent(self, store: SimulationSessionStore):
        assert store.get("nonexistent") is None

    def test_list(self, store: SimulationSessionStore):
        s1 = self._make_session("s1")
        s2 = self._make_session("s2")
        store.save(s1)
        store.save(s2)
        assert len(store.list()) == 2
