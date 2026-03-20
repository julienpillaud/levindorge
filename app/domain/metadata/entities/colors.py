from enum import StrEnum

from app.domain.commons.category_groups import CategoryGroupName


class ArticleColor(StrEnum):
    AMBER_BEER = "Ambrée"
    WHITE_BEER = "Blanche"
    BLONDE_BEER = "Blonde"
    BROWN_BEER = "Brune"
    FRUITY_BEER = "Fruitée"
    WHITE_WINE = "Blanc"
    ROSE_WINE = "Rosé"
    RED_WINE = "Rouge"

    @classmethod
    def from_category(cls, name: CategoryGroupName) -> list[ArticleColor]:
        if name == CategoryGroupName.BEER:
            return [color for color in cls if color.name.endswith("_BEER")]
        elif name == CategoryGroupName.WINE:
            return [color for color in cls if color.name.endswith("_WINE")]
        else:
            return []
