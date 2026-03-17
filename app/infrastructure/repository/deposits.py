from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.deposits.entities import Deposit
from app.domain.deposits.repository import DepositRepositoryProtocol


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

    def exists(self, deposit: Deposit, /) -> bool:
        return self.collection.count_documents(deposit.model_dump(exclude={"id"})) > 0
