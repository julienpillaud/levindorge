import datetime
from typing import Literal

from pydantic import BaseModel

from app.domain.entities import DomainModel


class ArticleType(BaseModel):
    name: str
    category: str
    tax: float
    ratio_category: str
    list_category: str
    volume_category: str | None = None
    tactill_category: str


class ArticleName(BaseModel):
    name1: str
    name2: str


class ArticleVolume(BaseModel):
    value: float
    unit: Literal["cL", "L"]


class ArticleDeposit(BaseModel):
    unit: float
    case: float


class ArticleShopDetail(BaseModel):
    sell_price: float
    bar_price: float
    stock_quantity: int


class Article(DomainModel):
    type: str
    name: ArticleName
    buy_price: float
    excise_duty: float = 0.0
    social_security_levy: float = 0.0
    tax: float
    distributor: str
    barcode: str = ""
    region: str = ""
    color: str = ""
    taste: str = ""
    volume: ArticleVolume | None
    alcohol_by_volume: float = 0.0
    packaging: int = 0
    deposit: ArticleDeposit
    food_pairing: list[str]
    biodynamic: str = ""
    validated: bool
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    shops: dict[str, ArticleShopDetail]
