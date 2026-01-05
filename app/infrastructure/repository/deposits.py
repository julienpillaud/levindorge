from app.domain.deposits.entities import Deposit
from app.domain.deposits.repository import DepositRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class DepositRepository(MongoRepository[Deposit], DepositRepositoryProtocol):
    domain_entity_type = Deposit
    collection_name = "deposits"
    searchable_fields = ()

    def exists(self, deposit: Deposit, /) -> bool:
        return self.collection.count_documents(deposit.model_dump(exclude={"id"})) > 0
