from pydantic import BaseModel

from app.domain.entities import DomainModel


class DepositField(BaseModel):
    case: bool
    unit: bool


class CategoryGroup(DomainModel):
    slug: str
    title: str
    producer: str
    product: str | None
    region: str | None
    color: bool
    taste: bool
    volume: bool = True
    alcohol_by_volume: bool = True
    recommended_price: bool = True
    distributor: bool = True
    packaging: bool = False
    deposit: DepositField | None = None
    category: bool = False


class NonDrinkCategoryGroup(CategoryGroup):
    producer: str = "Produit"
    product: str | None = None
    region: str | None = None
    color: bool = False
    taste: bool = False
    volume: bool = False
    alcohol_by_volume: bool = False
    recommended_price: bool = False


class BeerLikeCategoryGroup(CategoryGroup):
    producer: str = "Brasserie"
    product: str = "Bière"
    region: str | None = "Pays"
    color: bool = True
    taste: bool = False


class SpiritLikeCategoryGroup(CategoryGroup):
    producer: str = "Distillerie"
    product: str = "Spiritueux"
    region: str | None = "Pays"
    color: bool = False
    taste: bool = True


class WineLikeCategoryGroup(CategoryGroup):
    producer: str = "Appellation"
    product: str = "Vin"
    region: str | None = "Région"
    color: bool = True
    taste: bool = False
    alcohol_by_volume: bool = False
