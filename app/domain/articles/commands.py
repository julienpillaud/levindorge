import datetime

from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import Article, ArticleCreateOrUpdate
from app.domain.commons.entities import DisplayGroup
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.users.entities import User


def get_articles_command(context: ContextProtocol) -> list[Article]:
    return context.repository.get_all_articles()


def get_articles_by_display_group_command(
    context: ContextProtocol,
    display_group: DisplayGroup,
) -> list[Article]:
    return context.repository.get_articles_by_display_group(display_group=display_group)


def get_article_command(context: ContextProtocol, article_id: str) -> Article:
    article = context.repository.get_article(article_id=article_id)
    if not article:
        raise NotFoundError()

    return article


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
    created_article = context.repository.create_article(article=article)

    for shop in context.repository.get_shops():
        context.event_publisher.publish(
            "create.article",
            {"shop": shop, "article": created_article},
        )

    return created_article


def update_article_command(
    context: ContextProtocol,
    current_user: User,
    article_id: EntityId,
    data: ArticleCreateOrUpdate,
) -> Article:
    existing_article = context.repository.get_article(article_id=article_id)
    if not existing_article:
        raise NotFoundError()

    article = Article(
        id=existing_article.id,
        **data.model_dump(),
        validated=existing_article.validated,
        created_by=current_user.name,
        created_at=existing_article.created_at,
        updated_at=datetime.datetime.now(datetime.UTC),
    )

    updated_article = context.repository.update_article(article=article)

    for shop in context.repository.get_shops():
        context.event_publisher.publish(
            "update.article",
            {"shop": shop, "article": updated_article},
        )

    return updated_article


def delete_article_command(
    context: ContextProtocol,
    article_id: EntityId,
) -> None:
    article = context.repository.get_article(article_id=article_id)
    if not article:
        raise NotFoundError()

    context.repository.delete_article(article=article)

    for shop in context.repository.get_shops():
        context.event_publisher.publish(
            "delete.article",
            {"shop": shop, "article_id": article_id},
        )
