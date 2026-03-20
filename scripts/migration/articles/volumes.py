from typing import Any

from pydantic import PositiveFloat

from app.domain.commons.category_groups import CategoryGroup
from app.domain.metadata.entities.volumes import ArticleVolume, VolumeUnit


def get_volume(
    article: dict[str, Any],
    /,
    category_group: CategoryGroup,
) -> ArticleVolume | None:
    if not article["volume"] or not category_group.volume:
        return None

    value, unit = convert_volume(
        value=article["volume"]["value"],
        unit=article["volume"]["unit"],
    )
    return ArticleVolume(value=value, unit=unit)


def convert_volume(value: float, unit: str) -> tuple[PositiveFloat, VolumeUnit]:
    if unit == VolumeUnit.CENTILITER and value >= 100:  # noqa: PLR2004
        value /= 100
        unit = VolumeUnit.LITER
    return value, VolumeUnit(unit)
