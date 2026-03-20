from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.repositories import DepositRepositoryProtocol


class DepositRepository(MongoRepository[Deposit], DepositRepositoryProtocol):
    domain_entity_type = Deposit
    collection_name = "deposits"
    searchable_fields = ()

    def create_many(self, deposits: list[Deposit]) -> list[Deposit]:
        entities = [self._to_database_entity(entity) for entity in deposits]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return deposits
