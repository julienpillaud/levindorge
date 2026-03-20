import random
import uuid
from typing import Any

from cleanstack.factories.mongo import BaseMongoFactory

from app.domain.metadata.entities.volumes import Volume, VolumeUnit
from app.infrastructure.repository.volumes import VolumeRepository


def generate_volume(**kwargs: Any) -> Volume:
    return Volume(
        id=kwargs["id"] if "id" in kwargs else uuid.uuid7(),
        value=kwargs["value"] if "value" in kwargs else random.randint(1, 1000),
        unit=kwargs["unit"] if "unit" in kwargs else random.choice(list(VolumeUnit)),
    )


class VolumeFactory(BaseMongoFactory[Volume]):
    def build(self, **kwargs: Any) -> Volume:
        return generate_volume(**kwargs)

    @property
    def _repository(self) -> VolumeRepository:
        return VolumeRepository(
            database=self.context.database,
            session=self.uow.session,
        )
