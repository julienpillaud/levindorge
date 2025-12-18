from app.domain.producers.entities import Producer
from app.domain.producers.repository import ProducerRepositoryProtocol
from app.infrastructure.repository.base import MongoRepository


class ProducerRepository(MongoRepository[Producer], ProducerRepositoryProtocol):
    domain_entity_type = Producer
    collection_name = "producers"
    searchable_fields = ()
