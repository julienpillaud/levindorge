from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse
from app.domain.volumes.entities import Volume, VolumeCategory, VolumeCreate


def get_volumes_command(
    context: ContextProtocol,
    volume_category: VolumeCategory,
) -> PaginatedResponse[Volume]:
    return context.volume_repository.get_all(
        filters={"category": volume_category},
        sort={"category": 1, "normalized_value": 1},
        limit=300,
    )


def create_volume_command(
    context: ContextProtocol,
    volume_create: VolumeCreate,
) -> Volume:
    volume = Volume(
        id="",
        value=volume_create.value,
        unit=volume_create.unit,
        category=volume_create.category,
    )

    # if context.repository.volume_exists(volume=volume):
    #     raise ConflictError()

    return context.volume_repository.create(volume)


def delete_volume_command(context: ContextProtocol, volume_id: EntityId) -> None:
    volume = context.volume_repository.get_by_id(volume_id)
    if not volume:
        raise NotFoundError()

    # if context.repository.volume_is_used(volume=volume):
    #     raise VolumeInUseError(item_name=volume.name)

    context.volume_repository.delete(volume)
