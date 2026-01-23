from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.pos.entities import POSArticleRequest
from app.domain.stores.entities import Store


def create_pos_article_command(
    context: ContextProtocol,
    data: POSArticleRequest,
) -> None:
    category = context.category_repository.get_by_name(name=data.article.category)
    if not category:
        raise NotFoundError("Category not found.")

    context.pos_manager.create_article(
        data.store,
        article=data.article,
        category=category,
    )


def update_pos_article_command(
    context: ContextProtocol,
    data: POSArticleRequest,
) -> None:
    category = context.category_repository.get_by_name(name=data.article.category)
    if not category:
        raise NotFoundError("Category not found.")

    context.pos_manager.update_article(
        data.store,
        article=data.article,
        category=category,
    )


def delete_pos_article_command(
    context: ContextProtocol,
    data: POSArticleRequest,
) -> None:
    context.pos_manager.delete_article(data.store, article=data.article)


def reset_pos_stocks_command(
    context: ContextProtocol,
    store: Store,
    category: str,
) -> None:
    context.pos_manager.reset_stocks_by_category(store, category=category)
