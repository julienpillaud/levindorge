from tactill import TactillColor

from app.domain.articles.entities import Article, ArticleColor
from app.domain.commons.entities import InventoryGroup

INCLUDED_CATEGORIES = [
    "ABSINTHE",
    "ACCESSOIRE",
    "ALIMENTATION",
    "ANISÉ",
    "ARMAGNAC",
    "BIB",
    "BIÈRE",
    "BSA",
    "CACHAÇA",
    "CIDRE",
    "COFFRET",
    "COGNAC",
    "EMBALLAGE",
    "FÛT",
    "GIN",
    "LIQUEUR",
    "MEZCAL",
    "MINI-FÛT",
    "RHUM",
    "RHUM ARRANGÉ",
    "VIN",
    "VIN EFFERVESCENT",
    "VIN MUTÉ",
    "VODKA",
    "WHISKY",
]
CATEGORIES_MAPPING = {
    "beer": ["BIÈRE", "CIDRE"],
    "keg": ["FÛT", "MINI-FÛT"],
    "spirit": [
        "ABSINTHE",
        "ANISÉ",
        "ARMAGNAC",
        "CACHAÇA",
        "COGNAC",
        "GIN",
        "LIQUEUR",
        "MEZCAL",
        "RHUM",
        "RHUM ARRANGÉ",
        "VODKA",
        "WHISKY",
    ],
    "wine": ["BIB", "VIN", "VIN EFFERVESCENT", "VIN MUTÉ"],
    "other": ["ACCESSOIRE", "ALIMENTATION", "BSA", "COFFRET", "EMBALLAGE"],
}
LITER_TO_CENTILITER = 100
COLORS_MAPPING = {
    ArticleColor.AMBER_BEER: TactillColor.ORANGE,
    ArticleColor.WHITE_BEER: TactillColor.GRAY,
    ArticleColor.BLONDE_BEER: TactillColor.YELLOW,
    ArticleColor.BROWN_BEER: TactillColor.BROWN,
    ArticleColor.FRUITY_BEER: TactillColor.PINK,
    ArticleColor.WHITE_WINE: TactillColor.GRAY,
    ArticleColor.ROSE_WINE: TactillColor.MAGENTA,
    ArticleColor.RED_WINE: TactillColor.PINK,
}


def define_name(display_group: InventoryGroup, article: Article) -> str:
    name1 = article.producer
    name2 = article.product
    volume = article.volume
    color = article.color

    match display_group:
        case InventoryGroup.BEER | InventoryGroup.CIDER:
            return f"{name2} {volume} {name1}" if name1 else f"{name2} {volume}"
        case (
            InventoryGroup.KEG
            | InventoryGroup.MINI_KEG
            | InventoryGroup.RUM
            | InventoryGroup.WHISKY
            | InventoryGroup.SPIRIT
            | InventoryGroup.ARRANGED
            | InventoryGroup.SPARKLING_WINE
        ):
            return f"{name1} {name2} {volume}" if name1 else f"{name2} {volume}"
        case InventoryGroup.BIB | InventoryGroup.WINE | InventoryGroup.FORTIFIED_WINE:
            if not name1:
                return f"{name2} {color} {volume}"
            if name2:
                return f"{name2} {color} {volume} {name1}"
            else:
                return f"{name1} {color} {volume}"
        case InventoryGroup.BOX | InventoryGroup.OTHER | InventoryGroup.FOOD:
            return name2
        case _:
            raise ValueError()


def define_icon_text(article: Article) -> str:
    if not article.volume:
        return "    "

    value, unit = article.volume.value, article.volume.unit
    if unit == "cL" and value > LITER_TO_CENTILITER:
        value = value / 100

    return str(value).rstrip("0").rstrip(".").ljust(4)


def define_color(display_group: InventoryGroup, article: Article) -> TactillColor:
    if not article.color:
        return TactillColor.GREEN

    match display_group:
        case (
            InventoryGroup.BEER
            | InventoryGroup.CIDER
            | InventoryGroup.KEG
            | InventoryGroup.MINI_KEG
        ):
            return COLORS_MAPPING[article.color]
        case InventoryGroup.RUM:
            return TactillColor.TEAL
        case InventoryGroup.WHISKY:
            return TactillColor.BLUE
        case InventoryGroup.SPIRIT | InventoryGroup.ARRANGED:
            return TactillColor.GRAY
        case (
            InventoryGroup.WINE
            | InventoryGroup.FORTIFIED_WINE
            | InventoryGroup.FORTIFIED_WINE
            | InventoryGroup.BIB
        ):
            return COLORS_MAPPING[article.color]
        case InventoryGroup.BOX:
            return TactillColor.MAGENTA
        case InventoryGroup.OTHER | InventoryGroup.FOOD:
            return TactillColor.GREEN
        case _:
            raise ValueError()
