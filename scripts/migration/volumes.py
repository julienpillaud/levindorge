import uuid

from pydantic import PositiveFloat
from rich import print

from app.core.context import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.commons.category_groups import CATEGORY_GROUPS_MAP
from app.domain.volumes.entities import Volume, VolumeCategory, VolumeUnit


def create_volume(
    dst_context: Context,
    categories: list[Category],
    articles: list[Article],
) -> None:
    # Create volumes with the new entity model
    dst_volumes = create_volume_entities(
        categories=categories,
        articles=articles,
    )

    # Save volumes in the database
    dst_context.volume_repository.create_many(dst_volumes)

    count = len(dst_volumes)
    print(f"Created {count} volumes")


def create_volume_entities(
    categories: list[Category],
    articles: list[Article],
) -> list[Volume]:
    categories_map = {category.name: category for category in categories}

    dst_volumes: dict[tuple[PositiveFloat, VolumeUnit, VolumeCategory], Volume] = {}
    for article in articles:
        if not article.volume:
            continue

        category = categories_map[article.category]
        category_group = CATEGORY_GROUPS_MAP[category.category_group]
        if not category_group.volume:
            continue

        key = (article.volume.value, article.volume.unit, category_group.volume)
        if key not in dst_volumes:
            dst_volumes[key] = Volume(
                id=uuid.uuid7(),
                value=article.volume.value,
                unit=VolumeUnit(article.volume.unit),
                category=category_group.volume,
            )

    return list(dst_volumes.values())
