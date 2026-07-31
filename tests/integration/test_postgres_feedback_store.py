import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_feedback_store_tests import AbstractFeedbackStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresFeedbackStore(AbstractFeedbackStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.feedback_store import PostgresFeedbackStore
        return PostgresFeedbackStore(migrated_db_url)
