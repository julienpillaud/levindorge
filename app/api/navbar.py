from pydantic import BaseModel

from app.domain.commons.entities import DisplayGroup
from app.domain.items.entities import ItemType


class NavbarCategory(BaseModel):
    code: DisplayGroup
    singular_name: str
    plural_name: str


class NavbarItem(BaseModel):
    label: str
    item_type: ItemType | None = None
    endpoint: str


navbar_categories = [
    NavbarCategory(
        code=DisplayGroup.BEER,
        singular_name="Bière",
        plural_name="Bières",
    ),
    NavbarCategory(
        code=DisplayGroup.CIDER,
        singular_name="Cidre",
        plural_name="Cidres",
    ),
    NavbarCategory(
        code=DisplayGroup.KEG,
        singular_name="Fût",
        plural_name="Fûts",
    ),
    NavbarCategory(
        code=DisplayGroup.MINI_KEG,
        singular_name="Mini-fût",
        plural_name="Mini-fûts",
    ),
    NavbarCategory(
        code=DisplayGroup.RHUM,
        singular_name="Rhum",
        plural_name="Rhums",
    ),
    NavbarCategory(
        code=DisplayGroup.WHISKY,
        singular_name="Whisky",
        plural_name="Whiskys",
    ),
    NavbarCategory(
        code=DisplayGroup.ARRANGED,
        singular_name="Arrangé",
        plural_name="Arrangés",
    ),
    NavbarCategory(
        code=DisplayGroup.SPIRIT,
        singular_name="Spiritueux",
        plural_name="Spiritueux",
    ),
    NavbarCategory(
        code=DisplayGroup.WINE,
        singular_name="Vin",
        plural_name="Vins",
    ),
    NavbarCategory(
        code=DisplayGroup.FORTIFIED_WINE,
        singular_name="Vin muté",
        plural_name="Vins mutés",
    ),
    NavbarCategory(
        code=DisplayGroup.SPARKLING_WINE,
        singular_name="Vin effervescent",
        plural_name="Vins effervescents",
    ),
    NavbarCategory(
        code=DisplayGroup.BIB,
        singular_name="BIB",
        plural_name="BIB",
    ),
    NavbarCategory(
        code=DisplayGroup.BOX,
        singular_name="Coffret",
        plural_name="Coffrets",
    ),
    NavbarCategory(
        code=DisplayGroup.FOOD,
        singular_name="Alimentation / BSA",
        plural_name="Alimentation / BSA",
    ),
    NavbarCategory(
        code=DisplayGroup.MISC,
        singular_name="Accessoire / Emballage",
        plural_name="Accessoires / Emballages",
    ),
]

navbar_items = [
    NavbarItem(
        label="Fournisseurs",
        item_type=ItemType.DISTRIBUTORS,
        endpoint="get_items_view",
    ),
    NavbarItem(
        label="Volumes",
        endpoint="get_volumes_view",
    ),
    NavbarItem(
        label="Consignes",
        endpoint="get_deposits_view",
    ),
]
