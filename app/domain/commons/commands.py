from app.domain.articles.entities import ArticleColor, ArticleTaste
from app.domain.commons.category_groups import CategoryGroup
from app.domain.commons.entities import ViewData
from app.domain.context import ContextProtocol
from app.domain.deposits.commands import get_deposits_command
from app.domain.deposits.entities import Deposit
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
    category_group: CategoryGroup,
) -> ViewData:
    return ViewData(
        producers=get_producers(context, category_group=category_group),
        distributors=get_distributors(context),
        colors=get_colors(category_group=category_group),
        tastes=get_tastes(),
        origins=get_origins(context),
        volumes=get_volumes(context, category_group=category_group),
        deposits=get_deposits(context, category_group=category_group),
    )


def get_producers(
    context: ContextProtocol,
    /,
    category_group: CategoryGroup,
) -> list[Producer]:
    if not category_group.producer:
        return []

    result = get_producers_command(
        context,
        producer_type=category_group.producer.type,
    )
    return result.items


def get_distributors(context: ContextProtocol, /) -> list[Distributor]:
    result = get_distributors_command(context)
    return result.items


def get_colors(category_group: CategoryGroup) -> list[ArticleColor]:
    if not category_group.color:
        return []

    return ArticleColor.from_category(category_group.color.category)


def get_tastes() -> list[ArticleTaste]:
    return list(ArticleTaste)


def get_origins(context: ContextProtocol, /) -> list[Origin]:
    result = get_origins_command(context)
    return result.items


def get_volumes(
    context: ContextProtocol,
    /,
    category_group: CategoryGroup,
) -> list[Volume]:
    if not category_group.volume:
        return []

    result = get_volumes_command(context, volume_category=category_group.volume)
    return result.items


def get_deposits(
    context: ContextProtocol,
    /,
    category_group: CategoryGroup,
) -> list[Deposit]:
    if not category_group.deposit:
        return []

    result = get_deposits_command(
        context=context,
        deposit_category=category_group.deposit.category,
    )
    return result.items
