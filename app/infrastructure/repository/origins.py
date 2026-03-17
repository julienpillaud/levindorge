from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.origins.entities import Origin
from app.domain.origins.repository import OriginRepositoryProtocol


class OriginRepository(MongoRepository[Origin], OriginRepositoryProtocol):
    domain_entity_type = Origin
    collection_name = "origins"
    searchable_fields = ()

    def create_many(self, origins: list[Origin]) -> list[Origin]:
        entities = [self._to_database_entity(entity) for entity in origins]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return origins

    def get_by_name(self, name: str) -> Origin | None:
        origin = self.collection.find_one({"name": name})
        return self._to_domain_entity(origin) if origin else None

    def exists(self, origin: Origin) -> bool:
        return self.collection.count_documents(origin.model_dump(exclude={"id"})) > 0
