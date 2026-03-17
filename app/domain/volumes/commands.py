import uuid

from cleanstack.domain import NotFoundError
from cleanstack.entities import (
    EntityId,
    FilterEntity,
    PaginatedResponse,
    Pagination,
    SortEntity,
    SortOrder,
)

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.exceptions import AlreadyExistsError, EntityInUseError
from app.domain.volumes.entities import Volume, VolumeCategory, VolumeCreate


@cached_command(response_model=PaginatedResponse[Volume], tag="volumes")
def get_volumes_command(
    context: ContextProtocol,
    /,
    category: VolumeCategory | None = None,
) -> PaginatedResponse[Volume]:
    filters = [FilterEntity(field="category", value=category)] if category else []
    return context.volume_repository.get_all(
        filters=filters,
        sort=[
            SortEntity(field="category", order=SortOrder.ASC),
            SortEntity(field="normalized_value", order=SortOrder.ASC),
        ],
        pagination=Pagination(page=1, size=300),
    )


def create_volume_command(
    context: ContextProtocol,
    /,
    volume_create: VolumeCreate,
) -> Volume:
    volume = Volume(
        id=uuid.uuid7(),
        value=volume_create.value,
        unit=volume_create.unit,
        category=volume_create.category,
    )
    if context.volume_repository.exists(volume):
        raise AlreadyExistsError(
            f"`{volume.display_name}` already exists.",
            volume.display_name,
        )

    created_volume = context.volume_repository.create(volume)
    context.cache_manager.invalidate_tag("volumes")
    return created_volume


def delete_volume_command(
    context: ContextProtocol,
    /,
    volume_id: EntityId,
) -> None:
    volume = context.volume_repository.get_by_id(volume_id)
    if not volume:
        raise NotFoundError(f"Volume `{volume_id}` not found.")

    if context.article_repository.exists_by_volume(volume):
        raise EntityInUseError(
            f"`{volume.display_name}` is still in use.",
            volume.display_name,
        )

    context.volume_repository.delete(volume)
    context.cache_manager.invalidate_tag("volumes")
