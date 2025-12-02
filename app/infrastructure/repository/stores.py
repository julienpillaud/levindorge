from app.domain.stores.entities import Store
from app.domain.stores.repository import StoreRepositoryProtocol
from app.domain.types import StoreSlug
from app.infrastructure.repository.mongo_repository import MongoRepository


class StoreRepository(MongoRepository[Store], StoreRepositoryProtocol):
    domain_entity_type = Store
    collection_name = "stores"
    searchable_fields = ()

    def get_by_slug(self, slug: StoreSlug) -> Store | None:
        store = self.collection.find_one({"slug": slug})
        return self._to_domain_entity(store) if store else None
