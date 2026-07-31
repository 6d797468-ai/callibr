import pytest
from callibr_persistence.memory.simulation_turn_store import MemorySimulationTurnStore

from tests.unit.persistence.abstract_simulation_turn_store_tests import AbstractSimulationTurnStoreTests


class TestMemorySimulationTurnStore(AbstractSimulationTurnStoreTests):
    @pytest.fixture
    def store(self):
        return MemorySimulationTurnStore()
