import datetime
import uuid

from cleanstack.exceptions import NotFoundError
from pydantic import PositiveInt

from app.domain.articles.entities import (
    Article,
    ArticleCreateOrUpdate,
)
from app.domain.context import ContextProtocol
from app.domain.entities import (
    DEFAULT_PAGINATION_SIZE,
    EntityId,
    PaginatedResponse,
    Pagination,
    QueryParams,
)
from app.domain.protocols.event_publisher import Event
from app.domain.stores.entities import Store
from app.domain.types import StoreSlug


def get_articles_command(
    context: ContextProtocol,
    /,
    search: str | None = None,
    page: PositiveInt = 1,
    limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(
        query=QueryParams(search=search),
        pagination=Pagination(page=page, limit=limit),
    )


def get_articles_by_ids_command(
    context: ContextProtocol,
    /,
    article_ids: list[EntityId],
) -> PaginatedResponse[Article]:
    return context.article_repository.get_by_ids(article_ids)


def get_article_command(context: ContextProtocol, /, article_id: EntityId) -> Article:
    article = context.article_repository.get_by_id(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    return article


def create_article_command(
    context: ContextProtocol,
    /,
    data: ArticleCreateOrUpdate,
) -> Article:
    if not context.category_repository.get_by_name(data.category):
        raise NotFoundError(f"Category '{data.category}' not found.")

    current_time = datetime.datetime.now(datetime.UTC)
    reference = uuid.uuid7()
    article = Article(
        **data.model_dump(),
        reference=reference,
        created_at=current_time,
        updated_at=current_time,
    )
    created_article = context.article_repository.create(article)

    stores = _get_stores(context, store_slugs=list(data.store_data.keys()))
    context.event_publisher.publish(
        events=[
            Event(
                queue="create.article",
                message={"store": store, "article": created_article},
            )
            for store in stores
        ]
    )

    return created_article


def update_article_command(
    context: ContextProtocol,
    /,
    article_id: EntityId,
    data: ArticleCreateOrUpdate,
) -> Article:
    if not context.category_repository.get_by_name(data.category):
        raise NotFoundError(f"Category '{data.category}' not found.")

    existing_article = context.article_repository.get_by_id(article_id)
    if not existing_article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    article = Article(
        id=existing_article.id,
        **data.model_dump(),
        reference=existing_article.reference,
        created_at=existing_article.created_at,
        updated_at=datetime.datetime.now(datetime.UTC),
    )

    updated_article = context.article_repository.update(article)

    stores = _get_stores(context, store_slugs=list(data.store_data.keys()))
    context.event_publisher.publish(
        events=[
            Event(
                queue="update.article",
                message={"store": store, "article": updated_article},
            )
            for store in stores
        ]
    )

    return updated_article


def delete_article_command(context: ContextProtocol, /, article_id: EntityId) -> None:
    article = context.article_repository.get_by_id(article_id)
    if not article:
        raise NotFoundError(f"Article '{article_id}' not found.")

    context.article_repository.delete(article)

    stores = _get_stores(context, store_slugs=list(article.store_data.keys()))
    context.event_publisher.publish(
        events=[
            Event(
                queue="delete.article",
                message={"store": store, "article": article},
            )
            for store in stores
        ]
    )


def _get_stores(
    context: ContextProtocol,
    /,
    store_slugs: list[StoreSlug],
) -> list[Store]:
    stores: list[Store] = []
    for store_slug in store_slugs:
        store = context.store_repository.get_by_slug(store_slug)
        if not store:
            raise NotFoundError("Store not found.")
        stores.append(store)
    return stores
