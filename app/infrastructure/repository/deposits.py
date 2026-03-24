from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.repositories import DepositRepositoryProtocol


class DepositRepository(MongoRepository[Deposit], DepositRepositoryProtocol):
    domain_entity_type = Deposit
    collection_name = "deposits"
    searchable_fields = ()
