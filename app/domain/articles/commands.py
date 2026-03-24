import datetime
import uuid

from cleanstack.domain import NotFoundError
from cleanstack.entities import (
    DEFAULT_PAGINATION_SIZE,
    EntityId,
    PaginatedResponse,
    Pagination,
)
from pydantic import PositiveInt

from app.domain.articles.entities import (
    Article,
    ArticleCreateOrUpdate,
)
from app.domain.context import ContextProtocol
from app.domain.protocols.event_publisher import Event
from app.domain.stores.commands import get_stores_by_slug_command


def get_articles_command(
    context: ContextProtocol,
    /,
    search: str | None = None,
    page: PositiveInt = 1,
    limit: PositiveInt = DEFAULT_PAGINATION_SIZE,
) -> PaginatedResponse[Article]:
    return context.article_repository.get_all(
        search=search,
        pagination=Pagination(page=page, size=limit),
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

    if data.producer and not context.producer_repository.get_by_name(data.producer):
        raise NotFoundError(f"Producer '{data.producer}' not found.")

    if not context.distributor_repository.get_by_name(data.distributor):
        raise NotFoundError(f"Distributor '{data.distributor}' not found.")

    if data.origin and not context.origin_repository.get_by_name(data.origin.name):
        raise NotFoundError(f"Origin '{data.origin}' not found.")

    current_time = datetime.datetime.now(datetime.UTC)
    article = Article(
        id=uuid.uuid7(),
        reference=uuid.uuid7(),
        previous_id=None,  # new articles use reference, not previous_id
        **data.model_dump(),
        created_at=current_time,
        updated_at=current_time,
    )
    created_article = context.article_repository.create(article)

    stores = get_stores_by_slug_command(
        context,
        store_slugs=list(data.store_data.keys()),
    )
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
        # keep previous_id until while the app is not completely migrated
        previous_id=existing_article.previous_id,
        reference=existing_article.reference,
        created_at=existing_article.created_at,
        updated_at=datetime.datetime.now(datetime.UTC),
    )

    updated_article = context.article_repository.update(article)

    stores = get_stores_by_slug_command(
        context,
        store_slugs=list(data.store_data.keys()),
    )
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

    stores = get_stores_by_slug_command(
        context,
        store_slugs=list(article.store_data.keys()),
    )
    context.event_publisher.publish(
        events=[
            Event(
                queue="delete.article",
                message={"store": store, "article": article},
            )
            for store in stores
        ]
    )
