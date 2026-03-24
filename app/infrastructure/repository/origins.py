from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.repositories import OriginRepositoryProtocol


class OriginRepository(MongoRepository[Origin], OriginRepositoryProtocol):
    domain_entity_type = Origin
    collection_name = "origins"
    searchable_fields = ()

    def get_by_name(self, name: str) -> Origin | None:
        origin = self.collection.find_one({"name": name})
        return self._to_domain_entity(origin) if origin else None
