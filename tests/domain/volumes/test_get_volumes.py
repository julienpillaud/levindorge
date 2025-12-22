from app.domain.context import ContextProtocol
from app.domain.volumes.commands import get_volumes_command
from app.domain.volumes.entities import VolumeCategory
from tests.factories.volumes import VolumeFactory


def test_get_volumes(context: ContextProtocol, volume_factory: VolumeFactory) -> None:
    volumes_count = 3
    volume_factory.create_many(volumes_count)

    result = get_volumes_command(context)

    assert result.total == volumes_count
    volumes = result.items
    assert len(volumes) == volumes_count


def test_get_volumes_by_category(
    context: ContextProtocol,
    volume_factory: VolumeFactory,
) -> None:
    volumes_count = 3
    volume_factory.create_many(volumes_count, category=VolumeCategory.KEG)
    volume_factory.create_one(category=VolumeCategory.BEER)

    result = get_volumes_command(context, category=VolumeCategory.BEER)

    assert result.total == 1
    volumes = result.items
    assert len(volumes) == 1
