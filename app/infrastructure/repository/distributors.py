from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.metadata.entities.distributors import Distributor
from app.domain.metadata.repositories import DistributorRepositoryProtocol


class DistributorRepository(
    MongoRepository[Distributor], DistributorRepositoryProtocol
):
    domain_entity_type = Distributor
    collection_name = "distributors"
    searchable_fields = ()

    def get_by_name(self, name: str) -> Distributor | None:
        distributor = self.collection.find_one({"name": name})
        return self._to_domain_entity(distributor) if distributor else None
