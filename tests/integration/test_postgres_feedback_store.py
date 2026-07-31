import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_feedback_store_tests import AbstractFeedbackStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresFeedbackStore(AbstractFeedbackStoreTests):
    @pytest.fixture
    def store(self, migrated_db_url):
        from callibr_persistence.postgres.feedback_store import PostgresFeedbackStore
        return PostgresFeedbackStore(migrated_db_url)

    def test_maybe_roundtrip(self, store):
        from callibr_contracts.telemetry import FeedbackRecord

        store.submit(FeedbackRecord("s1", "t1", "l1", 4, 4, 3, 4, "maybe", "mitigé", "2026-07-31T10:00:00"))

        records = store.list()
        assert records[0].would_use_for_training == "maybe"
        assert store.count() == 1
        assert store.count_would_use()["maybe"] == 1
