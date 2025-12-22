from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.volumes.entities import Volume
from app.infrastructure.repository.volumes import VolumeRepository
from tests.factories.base import BaseMongoFactory


class VolumeEntityFactory(ModelFactory[Volume]): ...


class VolumeFactory(BaseMongoFactory[Volume]):
    repository_class = VolumeRepository

    def build(self, **kwargs: Any) -> Volume:
        return VolumeEntityFactory.build(**kwargs)
