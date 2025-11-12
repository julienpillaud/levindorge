from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo import MongoClient

from app.core.config import Settings
from app.domain.category_groups.entities import (
    BeerLikeCategoryGroup,
    DepositField,
    NonDrinkCategoryGroup,
    SpiritLikeCategoryGroup,
    WineLikeCategoryGroup,
)

settings = Settings()
client: MongoClient[MongoDocument] = MongoClient(settings.mongo_uri)


data = [
    BeerLikeCategoryGroup(
        id="",
        slug="beer",
        title="Bières",
        packaging=True,
        deposit=DepositField(unit=True, case=True),
    ),
    BeerLikeCategoryGroup(
        id="",
        slug="cider",
        title="Cidres",
        producer="Cidrerie",
        product="Cidre",
    ),
    BeerLikeCategoryGroup(
        id="",
        slug="keg",
        title="Fûts",
        deposit=DepositField(unit=True, case=False),
    ),
    BeerLikeCategoryGroup(
        id="",
        slug="mini_keg",
        title="Mini-fûts",
        deposit=DepositField(unit=True, case=False),
    ),
    SpiritLikeCategoryGroup(
        id="",
        slug="rhum",
        title="Rhums",
        product="Rhum",
    ),
    SpiritLikeCategoryGroup(
        id="",
        slug="whisky",
        title="Whiskys",
        product="Whisky",
    ),
    SpiritLikeCategoryGroup(
        id="",
        slug="arranged",
        title="Arrangés",
        color=False,
        taste=False,
    ),
    SpiritLikeCategoryGroup(
        id="",
        slug="spirit",
        title="Spiritueux",
        category=True,
    ),
    WineLikeCategoryGroup(
        id="",
        slug="wine",
        title="Vins",
    ),
    WineLikeCategoryGroup(
        id="",
        slug="fortified_wine",
        title="Vins mutés",
        category=True,
    ),
    WineLikeCategoryGroup(
        id="",
        slug="sparkling_wine",
        title="Vins effervescents",
    ),
    WineLikeCategoryGroup(
        id="",
        slug="bib",
        title="BIB",
    ),
    NonDrinkCategoryGroup(
        id="",
        slug="box",
        title="Coffrets",
    ),
    NonDrinkCategoryGroup(
        id="",
        slug="food",
        title="Alimentation / BSA",
    ),
    NonDrinkCategoryGroup(
        id="",
        slug="misc",
        title="Divers",
        category=True,
    ),
]

client[settings.mongo_database]["category_groups"].insert_many(
    [d.model_dump(exclude={"id"}) for d in data]
)
