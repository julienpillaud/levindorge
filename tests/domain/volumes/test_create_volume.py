import pytest

from app.domain.context import ContextProtocol
from app.domain.exceptions import AlreadyExistsError
from app.domain.volumes.commands import create_volume_command
from app.domain.volumes.entities import VolumeCreate
from tests.factories.volumes import VolumeFactory


def test_create_volume(
    context: ContextProtocol,
    volume_factory: VolumeFactory,
) -> None:
    volume_data = volume_factory.build()
    volume_create = VolumeCreate(**volume_data.model_dump())

    volume = create_volume_command(context, volume_create=volume_create)

    assert volume.value == volume_create.value
    assert volume.unit == volume_create.unit
    assert volume.category == volume_create.category


def test_create_volume_already_exists(
    context: ContextProtocol,
    volume_factory: VolumeFactory,
) -> None:
    volume = volume_factory.create_one()
    volume_create = VolumeCreate(
        value=volume.value,
        unit=volume.unit,
        category=volume.category,
    )
    with pytest.raises(AlreadyExistsError):
        create_volume_command(context, volume_create=volume_create)
