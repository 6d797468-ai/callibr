import pytest
from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_report_store_tests import AbstractReportStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresReportStore(AbstractReportStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.report_store import PostgresReportStore
        return PostgresReportStore(migrated_db_url)
