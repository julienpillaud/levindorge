import datetime

from cleanstack.exceptions import NotFoundError
from pydantic import PositiveInt

from app.domain.articles.entities import Article, ArticleCreateOrUpdate
from app.domain.context import ContextProtocol
from app.domain.entities import DEFAULT_PAGINATION_SIZE, EntityId, PaginatedResponse
from app.domain.users.entities import User


def get_articles_command(
    context: ContextProtocol,
    search: str | None = None,
    page: PositiveInt = 1,
    limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(
        search=search,
        page=page,
        limit=limit,
    )


def get_articles_by_display_group_command(
    context: ContextProtocol,
    display_group: str,
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
    if not context.category_repository.get_by_name(data.category):
        raise NotFoundError()

    for store_slug in data.store_data:
        if not context.store_repository.get_by_slug(store_slug):
            raise NotFoundError()

    current_time = datetime.datetime.now(datetime.UTC)
    article = Article(
        **data.model_dump(),
        created_at=current_time,
        updated_at=current_time,
    )
    created_article = context.article_repository.create(article)

    for store in current_user.stores:
        context.event_publisher.publish(
            "create.article",
            {"shop": store, "article": created_article},
        )

    return created_article


def update_article_command(
    context: ContextProtocol,
    current_user: User,
    article_id: EntityId,
    data: ArticleCreateOrUpdate,
) -> Article:
    if not context.category_repository.get_by_name(data.category):
        raise NotFoundError()

    for store_slug in data.store_data:
        if not context.store_repository.get_by_slug(store_slug):
            raise NotFoundError()

    existing_article = context.article_repository.get_by_id(article_id)
    if not existing_article:
        raise NotFoundError()

    article = Article(
        id=existing_article.id,
        **data.model_dump(),
        created_at=existing_article.created_at,
        updated_at=datetime.datetime.now(datetime.UTC),
    )

    updated_article = context.article_repository.update(article)

    for store in current_user.stores:
        context.event_publisher.publish(
            "update.article",
            {"shop": store, "article": updated_article},
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

    for store in current_user.stores:
        context.event_publisher.publish(
            "delete.article",
            {"shop": store, "article_id": article_id},
        )
