from rich import print

from app.core.core import Context
from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.volumes.entities import Volume, VolumeUnit


def create_volume(
    dst_context: Context,
    categories: list[Category],
    articles: list[Article],
) -> None:
    dst_volumes = create_volume_entities(
        categories=categories,
        articles=articles,
    )
    dst_context.volume_repository.create_many(dst_volumes)
    count = len(dst_volumes)
    print(f"Created {count} volumes")


def create_volume_entities(
    categories: list[Category],
    articles: list[Article],
) -> list[Volume]:
    categories_map = {category.name: category for category in categories}

    dst_volumes: list[Volume] = []
    for article in articles:
        if not article.volume:
            continue

        dst_volume = Volume(
            value=article.volume.value,
            unit=VolumeUnit(article.volume.unit),
            category=categories_map[article.category].volume_category,
        )
        if dst_volume not in dst_volumes:
            dst_volumes.append(dst_volume)

    return dst_volumes
