from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.metadata.entities.volumes import Volume
from app.domain.metadata.repositories import VolumeRepositoryProtocol


class VolumeRepository(MongoRepository[Volume], VolumeRepositoryProtocol):
    domain_entity_type = Volume
    collection_name = "volumes"
    searchable_fields = ()
