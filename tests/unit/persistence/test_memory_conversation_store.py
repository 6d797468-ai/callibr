import pytest
from callibr_persistence.conversation_store import InMemoryConversationStore

from tests.unit.persistence.abstract_conversation_store_tests import AbstractConversationStoreTests


class TestMemoryConversationStore(AbstractConversationStoreTests):
    @pytest.fixture
    def store(self):
        return InMemoryConversationStore()
