import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_product_event_store_tests import AbstractProductEventStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresProductEventStore(AbstractProductEventStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.product_event_store import PostgresProductEventStore
        return PostgresProductEventStore(migrated_db_url)
