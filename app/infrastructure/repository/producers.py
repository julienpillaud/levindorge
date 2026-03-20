from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.metadata.entities.producers import Producer
from app.domain.metadata.repositories import ProducerRepositoryProtocol


class ProducerRepository(MongoRepository[Producer], ProducerRepositoryProtocol):
    domain_entity_type = Producer
    collection_name = "producers"
    searchable_fields = ()

    def create_many(self, producers: list[Producer]) -> list[Producer]:
        entities = [self._to_database_entity(entity) for entity in producers]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return producers
