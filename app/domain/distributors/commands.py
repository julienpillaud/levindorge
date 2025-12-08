from app.domain.context import ContextProtocol
from app.domain.distributors.entities import Distributor
from app.domain.entities import PaginatedResponse


def get_distributors_command(
    context: ContextProtocol,
    /,
) -> PaginatedResponse[Distributor]:
    return context.distributor_repository.get_all(sort={"name": 1}, limit=300)
