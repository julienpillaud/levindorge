import random
from typing import Any

from app.domain.volumes.entities import Volume, VolumeCategory, VolumeUnit
from app.infrastructure.repository.volumes import VolumeRepository
from tests.factories.base import BaseMongoFactory


def generate_volume(**kwargs: Any) -> Volume:
    return Volume(
        value=kwargs["value"] if "value" in kwargs else random.randint(1, 1000),
        unit=kwargs["unit"] if "unit" in kwargs else random.choice(list(VolumeUnit)),
        category=kwargs["category"]
        if "category" in kwargs
        else random.choice(list(VolumeCategory)),
    )


class VolumeFactory(BaseMongoFactory[Volume]):
    repository_class = VolumeRepository

    def build(self, **kwargs: Any) -> Volume:
        return generate_volume(**kwargs)
