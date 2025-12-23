from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.producers.entities import Producer, ProducerType


@cached_command(response_model=PaginatedResponse[Producer], ttl=3600)
def get_producers_command(
    context: ContextProtocol,
    /,
    producer_type: ProducerType | None = None,
) -> PaginatedResponse[Producer]:
    filters = {"type": producer_type} if producer_type else None
    return context.producer_repository.get_all(
        filters=filters,
        sort={"name": 1},
        limit=300,
    )
