import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel

from app.domain.articles.entities import Article
from app.domain.commons.entities import PricingGroup


class PriceLabelCreate(BaseModel):
    article_id: str
    label_count: int


class PriceLabelWrapper(BaseModel):
    article: Article
    pricing_group: PricingGroup
    label_count: int


class PriceLabelFileType(StrEnum):
    LARGE = "Bières / Vins"
    SMALL = "Spiritueux"


class PriceLabelFileShop(StrEnum):
    ANGOULEME = "Angoulême"
    SAINTE_EULALIE = "Sainte-Eulalie"
    PESSAC = "Pessac"


class PriceLabelFile(BaseModel):
    id: int
    type: PriceLabelFileType
    shop: PriceLabelFileShop
    date: datetime.datetime
    file: str

    @classmethod
    def from_path(cls, path: Path) -> PriceLabelFile:
        number_of_parts = 5
        parts = path.stem.split("_")
        if len(parts) != number_of_parts:
            raise ValueError()

        date = datetime.datetime.strptime(
            f"{parts[3]} {parts[4]}",
            "%Y-%m-%d %H-%M-%S",
        )
        file_type = parts[0].upper()
        shop = parts[2].replace("-", "_").upper()
        return cls(
            id=int(parts[1]),
            type=PriceLabelFileType[file_type],
            shop=PriceLabelFileShop[shop],
            date=date,
            file=path.name,
        )
