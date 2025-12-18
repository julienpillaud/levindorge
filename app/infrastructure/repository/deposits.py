from app.domain.deposits.entities import Deposit
from app.domain.deposits.repository import DepositRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class DepositRepository(MongoRepository[Deposit], DepositRepositoryProtocol):
    domain_entity_type = Deposit
    collection_name = "deposits"
    searchable_fields = ()
