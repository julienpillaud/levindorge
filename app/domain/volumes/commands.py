from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import VolumeInUseError
from app.domain.volumes.entities import Volume, VolumeCreate


def get_volumes_command(context: ContextProtocol) -> list[Volume]:
    return context.repository.get_volumes()


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
    return context.repository.create_volume(volume=volume)


def delete_volume_command(context: ContextProtocol, volume_id: EntityId) -> None:
    volume = context.repository.get_volume(volume_id=volume_id)
    if not volume:
        raise NotFoundError()

    if context.repository.volume_is_used(volume=volume):
        raise VolumeInUseError(item_name=volume.name)

    context.repository.delete_volume(volume=volume)
