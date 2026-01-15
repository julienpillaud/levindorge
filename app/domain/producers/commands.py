from cleanstack.exceptions import NotFoundError

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination, QueryParams
from app.domain.exceptions import AlreadyExistsError, EntityInUseError
from app.domain.filters import FilterEntity
from app.domain.producers.entities import Producer, ProducerCreate, ProducerType


@cached_command(response_model=PaginatedResponse[Producer], tag="producers")
def get_producers_command(
    context: ContextProtocol,
    /,
    producer_type: ProducerType | None = None,
) -> PaginatedResponse[Producer]:
    filters = [FilterEntity(field="type", value=producer_type)] if producer_type else []

    return context.producer_repository.get_all(
        query=QueryParams(filters=filters, sort={"name": 1}),
        pagination=Pagination(page=1, limit=300),
    )


def create_producer_command(
    context: ContextProtocol,
    /,
    producer_create: ProducerCreate,
) -> Producer:
    producer = Producer(name=producer_create.name, type=producer_create.type)
    if context.producer_repository.exists(producer):
        raise AlreadyExistsError(
            f"`{producer.display_name}` already exists.",
            producer.display_name,
        )

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
        raise NotFoundError("Producer not found.")

    if context.article_repository.exists_by_producer(producer.name):
        raise EntityInUseError(
            f"Producer `{producer.display_name}` is still in use.",
            producer.display_name,
        )

    context.producer_repository.delete(producer)
    context.cache_manager.invalidate_tag("producers")
