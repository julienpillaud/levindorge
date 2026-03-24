from cleanstack.entities import (
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
    SortOrder,
)
from pydantic import BaseModel

from app.domain.caching import cached_command
from app.domain.commons.category_groups import CategoryGroup
from app.domain.context import ContextProtocol
from app.domain.metadata.entities.colors import ArticleColor
from app.domain.metadata.entities.deposits import Deposit
from app.domain.metadata.entities.distributors import Distributor
from app.domain.metadata.entities.origins import Origin
from app.domain.metadata.entities.producers import Producer, ProducerType
from app.domain.metadata.entities.tastes import ArticleTaste
from app.domain.metadata.entities.volumes import Volume


class MetaData(BaseModel):
    colors: list[ArticleColor]
    deposits: list[Deposit]
    distributors: list[Distributor]
    origins: list[Origin]
    producers: list[Producer]
    tastes: list[ArticleTaste]
    volumes: list[Volume]


def get_metadata_command(
    context: ContextProtocol,
    /,
    category_group: CategoryGroup,
) -> MetaData:
    producer_type = category_group.producer.type if category_group.producer else None
    return MetaData(
        colors=get_colors(category_group=category_group),
        deposits=get_deposits_command(context).items,
        distributors=get_distributors_command(context).items,
        origins=get_origins_command(context).items,
        producers=get_producers_command(context, producer_type=producer_type).items,
        tastes=list(ArticleTaste),
        volumes=get_volumes_command(context).items,
    )


def get_colors(category_group: CategoryGroup) -> list[ArticleColor]:
    if not category_group.color:
        return []

    return ArticleColor.from_category(category_group.name)


@cached_command(return_type=PaginatedResponse[Deposit], tag="deposits")
def get_deposits_command(context: ContextProtocol, /) -> PaginatedResponse[Deposit]:
    return context.deposit_repository.get_all(
        sort=[
            SortEntity(field="type", order=SortOrder.ASC),
            SortEntity(field="value", order=SortOrder.ASC),
        ],
        pagination=Pagination(page=1, size=300),
    )


@cached_command(return_type=PaginatedResponse[Distributor], tag="distributors")
def get_distributors_command(
    context: ContextProtocol,
    /,
) -> PaginatedResponse[Distributor]:
    return context.distributor_repository.get_all(
        sort=[SortEntity(field="name", order=SortOrder.ASC)],
        pagination=Pagination(page=1, size=300),
    )


@cached_command(return_type=PaginatedResponse[Origin], tag="origins")
def get_origins_command(context: ContextProtocol, /) -> PaginatedResponse[Origin]:
    return context.origin_repository.get_all(
        sort=[SortEntity(field="name", order=SortOrder.ASC)],
        pagination=Pagination(page=1, size=300),
    )


@cached_command(return_type=PaginatedResponse[Producer], tag="producers")
def get_producers_command(
    context: ContextProtocol,
    /,
    producer_type: ProducerType | None = None,
) -> PaginatedResponse[Producer]:
    filters = [FilterEntity(field="type", value=producer_type)] if producer_type else []
    return context.producer_repository.get_all(
        filters=filters,
        sort=[SortEntity(field="name", order=SortOrder.ASC)],
        pagination=Pagination(page=1, size=300),
    )


@cached_command(return_type=PaginatedResponse[Volume], tag="volumes")
def get_volumes_command(context: ContextProtocol, /) -> PaginatedResponse[Volume]:
    return context.volume_repository.get_all(
        sort=[SortEntity(field="normalized_value", order=SortOrder.ASC)],
        pagination=Pagination(page=1, size=300),
    )
