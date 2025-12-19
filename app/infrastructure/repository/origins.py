from app.domain.origins.entities import Origin
from app.domain.origins.repository import OriginRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class OriginRepository(MongoRepository[Origin], OriginRepositoryProtocol):
    domain_entity_type = Origin
    collection_name = "origins"
    searchable_fields = ()
