from cleanstack.exceptions import ConflictError, NotFoundError

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.producers.entities import Producer, ProducerType


@cached_command(response_model=PaginatedResponse[Producer], tag="producers")
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


def create_producer_command(
    context: ContextProtocol,
    /,
    name: str,
    producer_type: ProducerType,
) -> Producer:
    if context.producer_repository.exists(name=name, producer_type=producer_type):
        raise ConflictError()

    producer = Producer(name=name, type=producer_type)
    created_producer = context.producer_repository.create(producer)
    context.cache_manager.invalidate_tag("producers")
    return created_producer


def delete_producer_command(
    context: ContextProtocol,
    /,
    producer_id: str,
) -> None:
    producer = context.producer_repository.get_by_id(producer_id)
    if not producer:
        raise NotFoundError()

    if context.article_repository.exists_by_producer(producer.name):
        raise ConflictError()

    context.producer_repository.delete(producer)
    context.cache_manager.invalidate_tag("producers")
