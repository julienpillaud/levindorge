from app.domain.volumes.entities import Volume
from app.domain.volumes.repository import VolumeRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class VolumeRepository(MongoRepository[Volume], VolumeRepositoryProtocol):
    domain_entity_type = Volume
    collection_name = "volumes"
    searchable_fields = ()

    def exists(self, volume: Volume, /) -> bool:
        return self.collection.count_documents(volume.model_dump(exclude={"id"})) > 0
