from pydantic import BaseModel

from app.domain.entities import EntityId
from app.domain.types import StoreSlug


class PriceLabelItemRequest(BaseModel):
    article_id: EntityId
    label_count: int


class PriceLabelRequest(BaseModel):
    store_slug: StoreSlug
    data: list[PriceLabelItemRequest]
