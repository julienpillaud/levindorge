from typing import Literal

from pydantic import BaseModel

from app.domain.entities import DomainModel


class VolumeCreate(BaseModel):
    value: float
    unit: Literal["cL", "L"]
    category: str


class Volume(DomainModel):
    value: float
    unit: Literal["cL", "L"]
    category: str

    @property
    def name(self) -> str:
        return f"Volume {self.value:g} {self.unit}"
