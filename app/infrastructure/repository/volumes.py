from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.metadata.entities.volumes import Volume
from app.domain.metadata.repositories import VolumeRepositoryProtocol


class VolumeRepository(MongoRepository[Volume], VolumeRepositoryProtocol):
    domain_entity_type = Volume
    collection_name = "volumes"
    searchable_fields = ()

    def create_many(self, volumes: list[Volume]) -> list[Volume]:
        entities = [self._to_database_entity(entity) for entity in volumes]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return volumes
