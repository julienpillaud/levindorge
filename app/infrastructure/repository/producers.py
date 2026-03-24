from cleanstack.infrastructure.mongo.base import MongoRepository

from app.domain.metadata.entities.producers import Producer
from app.domain.metadata.repositories import ProducerRepositoryProtocol


class ProducerRepository(MongoRepository[Producer], ProducerRepositoryProtocol):
    domain_entity_type = Producer
    collection_name = "producers"
    searchable_fields = ()

    def get_by_name(self, name: str) -> Producer | None:
        producer = self.collection.find_one({"name": name})
        return self._to_domain_entity(producer) if producer else None
