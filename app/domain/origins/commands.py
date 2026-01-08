from cleanstack.exceptions import NotFoundError

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse
from app.domain.exceptions import AlreadyExistsError, EntityInUseError
from app.domain.origins.entities import Origin, OriginCreate


@cached_command(response_model=PaginatedResponse[Origin], tag="origins")
def get_origins_command(context: ContextProtocol, /) -> PaginatedResponse[Origin]:
    return context.origin_repository.get_all(sort={"name": 1}, limit=300)


def create_origin_command(
    context: ContextProtocol,
    /,
    origin_create: OriginCreate,
) -> Origin:
    origin = Origin(
        name=origin_create.name,
        code=origin_create.code,
        type=origin_create.type,
    )
    if context.origin_repository.exists(origin):
        raise AlreadyExistsError(
            f"`{origin.display_name}` already exists.",
            origin.display_name,
        )

    created_origin = context.origin_repository.create(origin)
    context.cache_manager.invalidate_tag("origins")
    return created_origin


def delete_origin_command(context: ContextProtocol, /, origin_id: EntityId) -> None:
    origin = context.origin_repository.get_by_id(origin_id)
    if not origin:
        raise NotFoundError(f"Origin `{origin_id}` not found.")

    if context.article_repository.exists_by_origin(origin):
        raise EntityInUseError(
            f"`{origin.display_name}` is still in use.",
            origin.display_name,
        )

    context.origin_repository.delete(origin)
    context.cache_manager.invalidate_tag("origins")
