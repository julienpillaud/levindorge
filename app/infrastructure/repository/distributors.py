from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.distributors.entities import Distributor
from app.domain.distributors.repository import DistributorRepositoryProtocol


class DistributorRepository(
    MongoRepository[Distributor],
    DistributorRepositoryProtocol,
):
    domain_entity_type = Distributor
    collection_name = "distributors"
    searchable_fields = ()

    def create_many(self, distributors: list[Distributor]) -> list[Distributor]:
        entities = [self._to_database_entity(entity) for entity in distributors]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return distributors

    def get_by_name(self, name: str) -> Distributor | None:
        distributor = self.collection.find_one({"name": name})
        return self._to_domain_entity(distributor) if distributor else None

    def exists(self, name: str) -> bool:
        return self.collection.count_documents({"name": name}) > 0
