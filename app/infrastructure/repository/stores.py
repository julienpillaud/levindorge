from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.stores.entities import Store
from app.domain.stores.repository import StoreRepositoryProtocol
from app.domain.types import StoreSlug


class StoreRepository(MongoRepository[Store], StoreRepositoryProtocol):
    domain_entity_type = Store
    collection_name = "stores"
    searchable_fields = ()

    def create_many(self, stores: list[Store]) -> list[Store]:
        db_entities = [self._to_database_entity(entity) for entity in stores]

        result = self.collection.insert_many(db_entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return stores

    def get_by_slug(self, slug: StoreSlug) -> Store | None:
        store = self.collection.find_one({"slug": slug})
        return self._to_domain_entity(store) if store else None
