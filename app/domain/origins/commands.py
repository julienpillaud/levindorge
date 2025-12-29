from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse
from app.domain.origins.entities import Origin


@cached_command(response_model=PaginatedResponse[Origin], tag="origins")
def get_origins_command(context: ContextProtocol, /) -> PaginatedResponse[Origin]:
    return context.origin_repository.get_all(sort={"name": 1}, limit=300)
