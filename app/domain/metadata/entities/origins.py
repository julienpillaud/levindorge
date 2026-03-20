from enum import StrEnum

from cleanstack.entities import DomainEntity
from pydantic import BaseModel


class OriginType(StrEnum):
    COUNTRY = "country"
    REGION = "region"


class BaseOrigin(BaseModel):
    name: str
    code: str | None = None
    type: OriginType = OriginType.COUNTRY

    def __str__(self) -> str:
        return self.name


class Origin(DomainEntity, BaseOrigin):
    pass


class ArticleOrigin(BaseOrigin):
    pass
