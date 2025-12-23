from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.stores.entities import Store


@cached_command(response_model=PaginatedResponse[Store], ttl=3600)
def get_stores_command(context: ContextProtocol, /) -> PaginatedResponse[Store]:
    return context.store_repository.get_all()
