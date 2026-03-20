from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.repositories import OriginRepositoryProtocol


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
