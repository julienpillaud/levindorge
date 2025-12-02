from cleanstack.exceptions import NotFoundError

from app.domain.commons.entities import DisplayGroup
from app.domain.context import ContextProtocol
from app.domain.pos.entities import POSArticleCreateOrUpdate, POSArticleDelete
from app.domain.stores.entities import Store


def create_pos_article_command(
    context: ContextProtocol,
    data: POSArticleCreateOrUpdate,
) -> None:
    category = context.category_repository.get_by_name(name=data.article.category)
    if not category:
        raise NotFoundError()

    context.pos_manager.create_article(
        data.store,
        article=data.article,
        category_name=category.tactill_category,
        # TODO
        display_group=DisplayGroup.BEER,
    )


def update_pos_article_command(
    context: ContextProtocol,
    data: POSArticleCreateOrUpdate,
) -> None:
    category = context.category_repository.get_by_name(name=data.article.category)
    if not category:
        raise NotFoundError()

    context.pos_manager.update_article(
        data.store,
        article=data.article,
        category_name=category.tactill_category,
        # TODO
        display_group=DisplayGroup.BEER,
    )


def delete_pos_article_command(
    context: ContextProtocol,
    data: POSArticleDelete,
) -> None:
    context.pos_manager.delete_article_by_reference(
        data.store,
        reference=data.article_id,
    )


def reset_pos_stocks_command(
    context: ContextProtocol,
    store: Store,
    category: str,
) -> None:
    context.pos_manager.reset_stocks_by_category(store, category=category)
