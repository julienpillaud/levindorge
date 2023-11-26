from pydantic import BaseModel, RootModel


class ShopMargin(BaseModel):
    ratio: float
    operator: str
    decimal_round: float


class ShopMargins(RootModel[dict[str, ShopMargin]]):
    root: dict[str, ShopMargin]

    def __getitem__(self, item: str) -> ShopMargin:
        return self.root[item]


class Shop(BaseModel):
    name: str
    username: str
    tactill_api_key: str
    margins: ShopMargins
