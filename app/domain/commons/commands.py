from app.domain.categories.entities import Category
from app.domain.commons.entities import ArticleType, ViewData
from app.domain.context import ContextProtocol
from app.domain.origins.commands import get_origins_command
from app.domain.origins.entities import Origin
from app.domain.producers.commands import get_producers_command
from app.domain.producers.entities import Producer


def get_view_data_command(
    context: ContextProtocol,
    category: Category,
) -> ViewData:
    return ViewData(
        producers=get_producers(context=context, category=category),
        origins=get_origins(context=context),
    )


def get_producers(
    context: ContextProtocol,
    category: Category,
) -> list[Producer]:
    if not category.producer_type:
        return []

    results = get_producers_command(
        context=context,
        producer_type=category.producer_type,
    )
    return results.items


def get_origins(context: ContextProtocol) -> list[Origin]:
    results = get_origins_command(context=context)
    return results.items


def get_article_type_command(context: ContextProtocol, name: str) -> ArticleType:
    return context.repository.get_article_type_by_name(name=name)
