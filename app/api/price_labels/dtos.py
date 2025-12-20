from pydantic import BaseModel

from app.domain.types import StoreSlug


class PriceLabelItemRequest(BaseModel):
    article_id: str
    label_count: int


class PriceLabelRequest(BaseModel):
    store_slug: StoreSlug
    data: list[PriceLabelItemRequest]
