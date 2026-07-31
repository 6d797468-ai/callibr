import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_simulation_turn_store_tests import AbstractSimulationTurnStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresSimulationTurnStore(AbstractSimulationTurnStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.simulation_turn_store import PostgresSimulationTurnStore
        return PostgresSimulationTurnStore(migrated_db_url)
