import datetime

from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import Article, ArticleCreateOrUpdate
from app.domain.commons.entities import DisplayGroup
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.users.entities import User


def get_articles_command(context: ContextProtocol) -> list[Article]:
    return context.article_repository.get_all(
        sort={"type": 1},
        pagination=Pagination(page=1, limit=1000),
    ).items


def get_articles_by_display_group_command(
    context: ContextProtocol,
    display_group: DisplayGroup,
) -> PaginatedResponse[Article]:
    return context.article_repository.get_by_display_group(display_group=display_group)


def get_article_command(context: ContextProtocol, article_id: EntityId) -> Article:
    article = context.article_repository.get_by_id(article_id)
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
        **data.model_dump(),
        validated=False,
        created_by=current_user.name,
        created_at=current_time,
        updated_at=current_time,
    )
    created_article = context.article_repository.create(article)

    for shop in current_user.shops:
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
    existing_article = context.article_repository.get_by_id(article_id)
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

    updated_article = context.article_repository.update(article)

    for shop in current_user.shops:
        context.event_publisher.publish(
            "update.article",
            {"shop": shop, "article": updated_article},
        )

    return updated_article


def delete_article_command(
    context: ContextProtocol,
    current_user: User,
    article_id: EntityId,
) -> None:
    article = context.article_repository.get_by_id(article_id)
    if not article:
        raise NotFoundError()

    context.article_repository.delete(article)

    for shop in current_user.shops:
        context.event_publisher.publish(
            "delete.article",
            {"shop": shop, "article_id": article_id},
        )
