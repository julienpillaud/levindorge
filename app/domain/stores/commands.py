from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.stores.entities import Store


def get_stores_command(context: ContextProtocol) -> PaginatedResponse[Store]:
    return context.store_repository.get_all()
