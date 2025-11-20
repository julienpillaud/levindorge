from app.core.core import Context
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CategoryGroupName
from app.domain.commons.entities import PricingGroup


def update_categories(dst_context: Context) -> None:
    dst_context.category_repository.create_many(data)


data = [
    # ----- beer -----
    Category(
        name="Bière",
        pricing_group=PricingGroup.BEER,
        category_group=CategoryGroupName.BEER,
        tactill_category="BIÈRE",
    ),
    Category(
        name="Cidre",
        pricing_group=PricingGroup.BEER,
        category_group=CategoryGroupName.BEER,
        tactill_category="CIDRE",
    ),
    Category(
        name="Fût",
        pricing_group=PricingGroup.KEG,
        category_group=CategoryGroupName.KEG,
        tactill_category="FÛT",
    ),
    Category(
        name="Mini-fût",
        pricing_group=PricingGroup.MINI_KEG,
        category_group=CategoryGroupName.KEG,
        tactill_category="MINI-FÛT",
    ),
    # ----- spirit -----
    Category(
        name="Rhum",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="RHUM",
    ),
    Category(
        name="Whisky",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="WHISKY",
    ),
    Category(
        name="Rhum arrangé",
        pricing_group=PricingGroup.ARRANGED,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="RHUM ARRANGÉ",
    ),
    Category(
        name="Absinthe",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="ABSINTHE",
    ),
    Category(
        name="Anisé",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="ANISÉ",
    ),
    Category(
        name="Armagnac",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="ARMAGNAC",
    ),
    Category(
        name="Cachaça",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="CACHAÇA",
    ),
    Category(
        name="Cognac",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="COGNAC",
    ),
    Category(
        name="Gin",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="GIN",
    ),
    Category(
        name="Liqueur",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="LIQUEUR",
    ),
    Category(
        name="Mezcal",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="MEZCAL",
    ),
    Category(
        name="Vodka",
        pricing_group=PricingGroup.SPIRIT,
        category_group=CategoryGroupName.SPIRIT,
        tactill_category="VODKA",
    ),
    # ----- wine -----
    Category(
        name="Vin",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN",
    ),
    Category(
        name="Madère",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN MUTÉ",
    ),
    Category(
        name="Pineau",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN MUTÉ",
    ),
    Category(
        name="Porto",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN MUTÉ",
    ),
    Category(
        name="Xérès",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN MUTÉ",
    ),
    Category(
        name="Vin effervescent",
        pricing_group=PricingGroup.WINE,
        category_group=CategoryGroupName.WINE,
        tactill_category="VIN EFFERVESCENT",
    ),
    Category(
        name="BIB",
        pricing_group=PricingGroup.BIB,
        category_group=CategoryGroupName.WINE,
        tactill_category="BIB",
    ),
    # ----- other -----
    Category(
        name="Coffret",
        pricing_group=PricingGroup.BOX,
        category_group=CategoryGroupName.OTHER,
        tactill_category="COFFRET",
    ),
    Category(
        name="Alimentation",
        pricing_group=PricingGroup.OTHER,
        category_group=CategoryGroupName.OTHER,
        tactill_category="ALIMENTATION",
    ),
    Category(
        name="BSA",
        pricing_group=PricingGroup.OTHER,
        category_group=CategoryGroupName.OTHER,
        tactill_category="BSA",
    ),
    Category(
        name="Accessoire",
        pricing_group=PricingGroup.OTHER,
        category_group=CategoryGroupName.OTHER,
        tactill_category="ACCESSOIRE",
    ),
    Category(
        name="Emballage",
        pricing_group=PricingGroup.OTHER,
        category_group=CategoryGroupName.OTHER,
        tactill_category="EMBALLAGE",
    ),
]
