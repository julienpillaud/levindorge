from app.domain.context import ContextProtocol
from app.domain.pos.entities import POSArticleCreateOrUpdate, POSArticleDelete


def create_pos_article_command(
    context: ContextProtocol,
    data: POSArticleCreateOrUpdate,
) -> None:
    article_type = context.repository.get_article_type_by_name(name=data.article.type)
    context.pos_manager.create_article(
        data.shop,
        article=data.article,
        category_name=article_type.tactill_category,
        display_group=article_type.display_group,
    )


def update_pos_article_command(
    context: ContextProtocol,
    data: POSArticleCreateOrUpdate,
) -> None:
    article_type = context.repository.get_article_type_by_name(name=data.article.type)
    context.pos_manager.update_article(
        data.shop,
        article=data.article,
        category_name=article_type.tactill_category,
        display_group=article_type.display_group,
    )


def delete_pos_article_command(
    context: ContextProtocol,
    data: POSArticleDelete,
) -> None:
    context.pos_manager.delete_article_by_reference(
        data.shop,
        reference=data.article_id,
    )
