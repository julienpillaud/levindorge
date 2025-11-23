from app.domain.categories.entities import Category
from app.domain.commons.entities import ArticleType, ViewData
from app.domain.context import ContextProtocol
from app.domain.producers.commands import get_producers_command
from app.domain.producers.entities import Producer


def get_view_data_command(
    context: ContextProtocol,
    category: Category,
) -> ViewData:
    return ViewData(producers=get_producers(context=context, category=category))


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
    producers = results.items
    producers.append(Producer(name="", type=category.producer_type))
    return producers


def get_article_type_command(context: ContextProtocol, name: str) -> ArticleType:
    return context.repository.get_article_type_by_name(name=name)
