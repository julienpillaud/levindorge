from cleanstack.domain import NotFoundError
from cleanstack.entities import PaginatedResponse

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.stores.entities import Store
from app.domain.types import StoreSlug


@cached_command(return_type=PaginatedResponse[Store], ttl=3600)
def get_stores_command(context: ContextProtocol, /) -> PaginatedResponse[Store]:
    return context.store_repository.get_all()


@cached_command(return_type=list[Store], ttl=3600)
def get_stores_by_slug_command(
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
