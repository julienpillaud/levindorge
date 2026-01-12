import pytest
from bson import ObjectId
from cleanstack.exceptions import NotFoundError

from app.domain.articles.entities import ArticleVolume
from app.domain.context import ContextProtocol
from app.domain.exceptions import EntityInUseError
from app.domain.volumes.commands import delete_volume_command
from tests.factories.articles import ArticleFactory
from tests.factories.volumes import VolumeFactory


def test_delete_volume(
    context: ContextProtocol,
    volume_factory: VolumeFactory,
) -> None:
    volume = volume_factory.create_one()

    delete_volume_command(context, volume_id=volume.id)

    assert context.volume_repository.get_by_id(volume.id) is None


def test_delete_volume_not_found(context: ContextProtocol) -> None:
    with pytest.raises(NotFoundError):
        delete_volume_command(context, volume_id=str(ObjectId()))


def test_delete_volume_in_use(
    context: ContextProtocol,
    article_factory: ArticleFactory,
    volume_factory: VolumeFactory,
) -> None:
    volume = volume_factory.create_one()
    article_factory.create_one(
        volume=ArticleVolume(value=volume.value, unit=volume.unit),
    )

    with pytest.raises(EntityInUseError):
        delete_volume_command(context, volume_id=volume.id)
