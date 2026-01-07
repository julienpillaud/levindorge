from cleanstack.exceptions import NotFoundError

from app.domain.caching import cached_command
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse
from app.domain.exceptions import AlreadyExistsError, EntityInUseError
from app.domain.volumes.entities import Volume, VolumeCategory, VolumeCreate


@cached_command(response_model=PaginatedResponse[Volume], tag="volumes")
def get_volumes_command(
    context: ContextProtocol,
    /,
    category: VolumeCategory | None = None,
) -> PaginatedResponse[Volume]:
    filters = {"category": category} if category else {}
    return context.volume_repository.get_all(
        filters=filters,
        sort={"category": 1, "normalized_value": 1},
        limit=300,
    )


def create_volume_command(
    context: ContextProtocol,
    /,
    volume_create: VolumeCreate,
) -> Volume:
    volume = Volume(
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
