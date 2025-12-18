from app.domain.distributors.entities import Distributor
from app.domain.distributors.repository import DistributorRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class DistributorRepository(
    MongoRepository[Distributor],
    DistributorRepositoryProtocol,
):
    domain_entity_type = Distributor
    collection_name = "distributors"
    searchable_fields = ()
