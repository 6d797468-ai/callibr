from __future__ import annotations

from callibr_persistence.providers.factory import PersistenceFactory


def test_factory_creates_memory_provider() -> None:
    provider = PersistenceFactory.create("memory")

    assert provider.simulation_store is not None
    assert provider.feedback_store is not None
    assert provider.analytics_store is not None
    assert provider.turn_store is not None
    assert provider.report_store is not None
    assert provider.conversation_store is not None


def test_factory_memory_provider_returns_fresh_stores_per_create() -> None:
    first = PersistenceFactory.create("memory")
    second = PersistenceFactory.create("memory")

    assert first.feedback_store is not second.feedback_store
    assert first.analytics_store is not second.analytics_store


def test_factory_requires_db_url_for_postgres() -> None:
    try:
        PersistenceFactory.create("postgres")
    except ValueError as exc:
        assert "db_url" in str(exc)
    else:
        raise AssertionError("expected ValueError for postgres without db_url")
