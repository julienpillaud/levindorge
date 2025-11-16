from typing import Any

from pydantic import BaseModel, model_validator


class PriceLabelItemRequest(BaseModel):
    article_id: str
    label_count: int


class PriceLabelRequest(BaseModel):
    data: list[PriceLabelItemRequest]

    @model_validator(mode="before")
    @classmethod
    def convert(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "data": [
                PriceLabelItemRequest(article_id=article_id, label_count=int(nb_tags))
                for article_id, nb_tags in data.items()
                if nb_tags
            ]
        }
