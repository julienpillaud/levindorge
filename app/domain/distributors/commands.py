from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.distributors.entities import Distributor
from app.domain.entities import PaginatedResponse


@cached_command(response_model=PaginatedResponse[Distributor], tag="distributors")
def get_distributors_command(
    context: ContextProtocol,
    /,
) -> PaginatedResponse[Distributor]:
    return context.distributor_repository.get_all(sort={"name": 1}, limit=300)
