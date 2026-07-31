from callibr_persistence.providers.base import PersistenceProvider
from callibr_persistence.providers.memory import MemoryPersistenceProvider
from callibr_persistence.providers.postgres import PostgresPersistenceProvider


class PersistenceFactory:
    @staticmethod
    def create(persistence_type: str, db_url: str | None = None) -> PersistenceProvider:
        if persistence_type == "postgres":
            if not db_url:
                raise ValueError("db_url is required for postgres persistence")
            return PostgresPersistenceProvider(db_url)
        
        return MemoryPersistenceProvider()
