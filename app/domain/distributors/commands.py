from cleanstack.exceptions import NotFoundError

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.distributors.entities import Distributor
from app.domain.entities import PaginatedResponse, Pagination, QueryParams
from app.domain.exceptions import AlreadyExistsError, EntityInUseError


@cached_command(response_model=PaginatedResponse[Distributor], tag="distributors")
def get_distributors_command(
    context: ContextProtocol,
    /,
) -> PaginatedResponse[Distributor]:
    return context.distributor_repository.get_all(
        query=QueryParams(sort={"name": 1}),
        pagination=Pagination(page=1, limit=300),
    )


def create_distributor_command(
    context: ContextProtocol,
    /,
    name: str,
) -> Distributor:
    distributor = Distributor(name=name)
    if context.distributor_repository.exists(name=name):
        raise AlreadyExistsError(
            f"`{distributor.display_name}` already exists.",
            distributor.display_name,
        )

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
        raise NotFoundError("Distributor not found.")

    if context.article_repository.exists_by_distributor(distributor.name):
        raise EntityInUseError(
            f"`{distributor.display_name}` is still in use.",
            distributor.display_name,
        )

    context.distributor_repository.delete(distributor)
    context.cache_manager.invalidate_tag("distributors")
