from cleanstack.exceptions import ConflictError, NotFoundError

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


def create_distributor_command(
    context: ContextProtocol,
    /,
    name: str,
) -> Distributor:
    if context.distributor_repository.exists(name=name):
        raise ConflictError()

    distributor = Distributor(name=name)
    created_distributor = context.distributor_repository.create(distributor)
    context.cache_manager.invalidate_tag("distributors")
    return created_distributor


def delete_distributor_command(
    context: ContextProtocol,
    /,
    distributor_id: str,
) -> None:
    distributor = context.distributor_repository.get_by_id(distributor_id)
    if not distributor:
        raise NotFoundError()

    if context.article_repository.exists_by_distributor(distributor.name):
        raise ConflictError()

    context.distributor_repository.delete(distributor)
    context.cache_manager.invalidate_tag("distributors")
