from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.volumes.entities import Volume
from app.domain.volumes.repository import VolumeRepositoryProtocol


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

    def exists(self, volume: Volume, /) -> bool:
        return self.collection.count_documents(volume.model_dump(exclude={"id"})) > 0
