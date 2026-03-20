from enum import StrEnum

from cleanstack.entities import DomainEntity
from pydantic import BaseModel, PositiveFloat, computed_field


class VolumeUnit(StrEnum):
    CENTILITER = "cL"
    LITER = "L"

    def to_centiliter(self, value: float) -> float:
        factors = {
            VolumeUnit.CENTILITER: 1,
            VolumeUnit.LITER: 100,
        }
        return value * factors[self]


class BaseVolume(BaseModel):
    value: PositiveFloat
    unit: VolumeUnit

    @computed_field(repr=False)
    @property
    def normalized_value(self) -> float:
        return self.unit.to_centiliter(self.value)

    def __str__(self) -> str:
        formatted_value = str(self.value).rstrip("0").rstrip(".").replace(".", ",")
        return f"{formatted_value} {self.unit}"


class Volume(DomainEntity, BaseVolume):
    pass


class ArticleVolume(BaseVolume):
    pass
