import datetime

from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import Article, ArticleCreateOrUpdate
from app.domain.commons.entities import DisplayGroup
from app.domain.context import ContextProtocol
from app.domain.entities import PyObjectId
from app.domain.shops.entities import Shop
from app.domain.users.entities import User


def get_articles_command(context: ContextProtocol) -> list[Article]:
    return context.repository.get_all_articles()


def get_articles_by_display_group_command(
    context: ContextProtocol,
    display_group: DisplayGroup,
) -> list[Article]:
    return context.repository.get_articles_by_list(display_group=display_group)


def get_article_command(context: ContextProtocol, article_id: str) -> Article:
    return context.repository.get_article(article_id=article_id)


def create_article_command(
    context: ContextProtocol,
    current_user: User,
    data: ArticleCreateOrUpdate,
) -> Article:
    current_time = datetime.datetime.now(datetime.UTC)
    article = Article(
        id="",
        **data.model_dump(),
        validated=False,
        created_by=current_user.name,
        created_at=current_time,
        updated_at=current_time,
    )
    article = context.repository.create_article(article=article)

    for shop in context.repository.get_shops():
        context.event_publisher.publish(
            "create.article",
            {"shop": shop, "article": article},
        )

    return article


def create_pos_article_command(
    context: ContextProtocol,
    shop: Shop,
    article: Article,
) -> None:
    article_type = context.repository.get_article_type_by_name(name=article.type)
    context.pos_manager.create_article(
        shop,
        article=article,
        category_name=article_type.tactill_category,
        display_group=article_type.display_group,
    )


def delete_article_command(context: ContextProtocol, article_id: PyObjectId) -> None:
    article = context.repository.get_article(article_id=article_id)
    if not article:
        raise NotFoundError()

    context.repository.delete_article(article=article)

    for shop in context.repository.get_shops():
        context.event_publisher.publish(
            "delete.article",
            {"shop": shop, "article_id": article_id},
        )


def delete_pos_article_command(
    context: ContextProtocol,
    shop: Shop,
    article_id: PyObjectId,
) -> None:
    context.pos_manager.delete_article_by_reference(shop, reference=article_id)
