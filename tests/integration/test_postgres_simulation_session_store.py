import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_simulation_session_store_tests import AbstractSimulationSessionStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresSimulationSessionStore(AbstractSimulationSessionStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.simulation_session_store import PostgresSimulationSessionStore
        return PostgresSimulationSessionStore(migrated_db_url)
