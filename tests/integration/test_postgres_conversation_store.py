import pytest

from tests.integration.conftest import skip_if_no_db
from tests.unit.persistence.abstract_conversation_store_tests import AbstractConversationStoreTests

pytestmark = [skip_if_no_db]


class TestPostgresConversationStore(AbstractConversationStoreTests):
    @pytest.fixture
    def store(self, db_url):
        from callibr_persistence.postgres.conversation_store import PostgresConversationStore
        s = PostgresConversationStore(db_url)
        s.init_schema()
        return s
