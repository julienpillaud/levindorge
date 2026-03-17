from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.producers.entities import Producer
from app.domain.producers.repository import ProducerRepositoryProtocol


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

    def get_by_name(self, name: str) -> Producer | None:
        producer = self.collection.find_one({"name": name})
        return self._to_domain_entity(producer) if producer else None

    def exists(self, producer: Producer, /) -> bool:
        return (
            self.collection.count_documents(
                {"name": producer.name, "type": producer.type}
            )
            > 0
        )
