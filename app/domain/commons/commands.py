from app.domain.categories.entities import Category
from app.domain.commons.entities import ArticleType, ViewData
from app.domain.context import ContextProtocol
from app.domain.distributors.commands import get_distributors_command
from app.domain.distributors.entities import Distributor
from app.domain.origins.commands import get_origins_command
from app.domain.origins.entities import Origin
from app.domain.producers.commands import get_producers_command
from app.domain.producers.entities import Producer
from app.domain.volumes.commands import get_volumes_command
from app.domain.volumes.entities import Volume


def get_view_data_command(
    context: ContextProtocol,
    category: Category,
) -> ViewData:
    return ViewData(
        producers=get_producers(context=context, category=category),
        distributors=get_distributors(context=context),
        origins=get_origins(context=context),
        volumes=get_volumes(context=context, category=category),
    )


def get_producers(context: ContextProtocol, category: Category) -> list[Producer]:
    if not category.producer_type:
        return []

    result = get_producers_command(
        context=context,
        producer_type=category.producer_type,
    )
    return result.items


def get_distributors(context: ContextProtocol) -> list[Distributor]:
    result = get_distributors_command(context=context)
    return result.items


def get_origins(context: ContextProtocol) -> list[Origin]:
    result = get_origins_command(context=context)
    return result.items


def get_volumes(
    context: ContextProtocol,
    category: Category,
) -> list[Volume]:
    if not category.volume_category:
        return []

    result = get_volumes_command(
        context=context,
        volume_category=category.volume_category,
    )
    return result.items


def get_article_type_command(context: ContextProtocol, name: str) -> ArticleType:
    return context.repository.get_article_type_by_name(name=name)
