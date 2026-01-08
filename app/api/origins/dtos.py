from pydantic import BaseModel

from app.domain.origins.entities import OriginType


class OriginDTO(BaseModel):
    name: str
    code: str | None
    type: OriginType
