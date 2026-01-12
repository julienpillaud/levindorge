from enum import StrEnum

from pydantic import BaseModel, PositiveFloat, computed_field

from app.domain.entities import DomainEntity


class VolumeUnit(StrEnum):
    CENTILITER = "cL"
    LITER = "L"

    def to_centiliter(self, value: float) -> float:
        factors = {
            VolumeUnit.CENTILITER: 1,
            VolumeUnit.LITER: 100,
        }
        return value * factors[self]


class VolumeCategory(StrEnum):
    BEER = "beer"
    KEG = "keg"
    SPIRIT = "spirit"
    WINE = "wine"

    @property
    def label(self) -> str:
        mapping = {
            VolumeCategory.BEER: "Bière",
            VolumeCategory.KEG: "Fût",
            VolumeCategory.SPIRIT: "Spiritueux",
            VolumeCategory.WINE: "Vin",
        }
        return mapping[self]


class Volume(DomainEntity):
    value: PositiveFloat
    unit: VolumeUnit
    category: VolumeCategory

    @computed_field(repr=False)  # type: ignore[prop-decorator]
    @property
    def normalized_value(self) -> float:
        return self.unit.to_centiliter(self.value)

    @property
    def display_name(self) -> str:
        formatted_value = str(self.value).rstrip("0").rstrip(".").replace(".", ",")
        return f"{formatted_value} {self.unit}"

    def __str__(self) -> str:
        formatted_value = str(self.value).rstrip("0").rstrip(".").replace(".", ",")
        return f"{formatted_value} {self.unit}"


class VolumeCreate(BaseModel):
    value: PositiveFloat
    unit: VolumeUnit
    category: VolumeCategory
