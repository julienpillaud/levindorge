from cleanstack.exceptions import NotFoundError

from app.core.config.settings import Settings
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse
from app.domain.origins.commands import get_origins_command
from app.domain.price_labels.entities import PriceLabelCreate, PriceLabelSheet
from app.domain.price_labels.utils.common import split_by_size
from app.domain.price_labels.utils.large import create_large_price_labels
from app.domain.price_labels.utils.small import create_small_price_labels
from app.domain.types import StoreSlug


def create_price_labels_command(
    context: ContextProtocol,
    /,
    settings: Settings,
    store_slug: StoreSlug,
    price_labels_create: list[PriceLabelCreate],
) -> None:
    store = context.store_repository.get_by_slug(store_slug)
    if not store:
        raise NotFoundError()

    large_price_labels, small_price_labels = split_by_size(
        context=context,
        price_labels=price_labels_create,
    )

    if large_price_labels:
        price_labels = create_large_price_labels(
            settings=settings,
            store=store,
            price_label_wrappers=large_price_labels,
        )
        context.price_label_repository.create_many(price_labels)

    if small_price_labels:
        origins = get_origins_command(context)
        origins_map = {origin.name: origin for origin in origins.items}
        price_labels = create_small_price_labels(
            store=store,
            price_label_wrappers=small_price_labels,
            origins_map=origins_map,
        )
        context.price_label_repository.create_many(price_labels)


def get_price_labels_command(
    context: ContextProtocol,
    /,
) -> PaginatedResponse[PriceLabelSheet]:
    return context.price_label_repository.get_all()


def get_price_labels_sheet_command(
    context: ContextProtocol,
    /,
    price_labels_id: EntityId,
) -> PriceLabelSheet:
    price_labels = context.price_label_repository.get_by_id(price_labels_id)
    if not price_labels:
        raise NotFoundError()

    return price_labels


def delete_price_labels_command(
    context: ContextProtocol,
    /,
    price_labels_id: EntityId,
) -> None:
    price_labels = context.price_label_repository.get_by_id(price_labels_id)
    if not price_labels:
        raise NotFoundError()

    context.price_label_repository.delete(price_labels)
