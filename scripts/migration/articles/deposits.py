from typing import Any

from app.domain.commons.category_groups import CategoryGroup
from app.domain.metadata.entities.deposits import ArticleDeposit


def get_deposit(
    article: dict[str, Any],
    /,
    category_group: CategoryGroup,
) -> ArticleDeposit | None:
    if not category_group.deposit:
        return None

    unit = article["deposit"]["unit"]
    if not unit:
        return None

    return ArticleDeposit(
        unit=unit,
        case=article["deposit"]["case"] or None,
        packaging=article["packaging"] or None,
    )
