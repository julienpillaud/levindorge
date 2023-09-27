from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

from application.entities.inventory import Inventory


class ArticleType(BaseModel):
    name: str
    category: str
    tax: float
    ratio_category: str
    list_category: str
    tactill_category: str


class ArticleName(BaseModel):
    name1: str
    name2: str


class ArticleDeposit(BaseModel):
    unit: float
    case: float


class ArticleShopDetail(BaseModel):
    sell_price: float
    bar_price: float
    stock_quantity: int


class ArticleShops(RootModel[dict[str, ArticleShopDetail]]):
    root: dict[str, ArticleShopDetail]

    def __getitem__(self, item: str) -> ArticleShopDetail:
        return self.root[item]


class RequestArticle(BaseModel):
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
    volume: float = 0.0
    alcohol_by_volume: float = 0.0
    packaging: int = 0
    deposit: ArticleDeposit
    food_pairing: list[str] = []
    biodynamic: str = ""

    @field_validator("excise_duty", "social_security_levy", mode="before")
    def empty_to_zero(cls, value: float | str) -> float:
        return 0.0 if value == "" else value

    @property
    def taxfree_price(self) -> float:
        taxfree_price_sum = sum(
            [self.buy_price, self.excise_duty, self.social_security_levy]
        )
        return round(taxfree_price_sum, 4)


class CreateOrUpdateArticle(RequestArticle):
    model_config = ConfigDict(extra="forbid")

    validated: bool
    created_by: str
    created_at: datetime
    updated_at: datetime
    shops: ArticleShops


class Article(CreateOrUpdateArticle):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def convert_objectid(cls, value: ObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Must be an ObjectId")
        return str(value)


class ArticleMargin(BaseModel):
    margin: float
    markup: float


class AugmentedArticle(Article):
    model_config = ConfigDict(extra="forbid")

    recommended_price: float
    margin: ArticleMargin


class InventoryArticle(Article):
    inventory: Inventory | None = None
