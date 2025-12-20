from app.domain.price_labels.entities import PriceLabelSheet
from app.domain.price_labels.repository import PriceLabelRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class PriceLabelRepository(
    MongoRepository[PriceLabelSheet], PriceLabelRepositoryProtocol
):
    domain_entity_type = PriceLabelSheet
    collection_name = "price_labels"
    searchable_fields = ()
