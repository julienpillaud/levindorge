import datetime
from enum import StrEnum

from pydantic import BaseModel

from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup
from app.domain.entities import DomainEntity
from app.domain.types import EntityId, StoreName


class PriceLabelCreate(BaseModel):
    article_id: EntityId
    label_count: int


class PriceLabelWrapper(BaseModel):
    article: Article
    pricing_group: PricingGroup
    label_count: int


class PriceLabelType(StrEnum):
    LARGE = "Bières / Vins"
    SMALL = "Spiritueux"


class PriceLabelSheet(DomainEntity):
    type: PriceLabelType
    store_name: StoreName
    index: int
    date: datetime.datetime
    content: str

    @property
    def slug(self) -> str:
        return self.type.name.lower()
