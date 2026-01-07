from pydantic import BaseModel

from app.domain.volumes.entities import VolumeCategory, VolumeUnit


class VolumeDTO(BaseModel):
    value: float
    unit: VolumeUnit
    category: VolumeCategory
