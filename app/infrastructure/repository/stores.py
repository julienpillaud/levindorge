from app.domain.stores.entities import Store
from app.domain.stores.repository import StoreRepositoryProtocol
from app.infrastructure.repository.mongo_repository import MongoRepository


class StoreRepository(MongoRepository[Store], StoreRepositoryProtocol):
    domain_model = Store
    collection_name = "stores"
    searchable_fields = ()
