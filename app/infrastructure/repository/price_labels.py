from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.price_labels.entities import PriceLabelSheet
from app.domain.price_labels.repository import PriceLabelRepositoryProtocol


class PriceLabelRepository(
    MongoRepository[PriceLabelSheet],
    PriceLabelRepositoryProtocol,
):
    domain_entity_type = PriceLabelSheet
    collection_name = "price_labels"
    searchable_fields = ()

    def create_many(self, price_labels: list[PriceLabelSheet]) -> list[PriceLabelSheet]:
        entities = [self._to_database_entity(entity) for entity in price_labels]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return price_labels
