import pytest
from callibr_persistence.session_store import InMemorySimulationSessionStore
from tests.unit.persistence.abstract_simulation_session_store_tests import AbstractSimulationSessionStoreTests

class TestMemorySimulationSessionStore(AbstractSimulationSessionStoreTests):
    @pytest.fixture
    def store(self):
        return InMemorySimulationSessionStore()
