from app.domain.producers.entities import Producer, ProducerType
from app.domain.producers.repository import ProducerRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class ProducerRepository(MongoRepository[Producer], ProducerRepositoryProtocol):
    domain_entity_type = Producer
    collection_name = "producers"
    searchable_fields = ()

    def exists(self, name: str, producer_type: ProducerType) -> bool:
        return (
            self.collection.count_documents({"name": name, "type": producer_type}) > 0
        )
