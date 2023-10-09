from pathlib import Path
from typing import Any

from application.entities.article import TagArticle
from application.entities.shop import Shop
from utils import mongo_db
from utils.tag import PriceTag

large_tag_category = {
    "beer",
    "cider",
    "mini_keg",
    "wine",
    "fortified_wine",
    "sparkling_wine",
    "bib",
    "box",
    "food",
    "misc",
}
small_tag_category = {"spirit", "arranged"}


class TagManager:
    @staticmethod
    def create(
        request_form: dict[str, Any], shop: Shop, tags_path: Path, fonts_path: Path
    ) -> None:
        large_tags, small_tags = build_tag_lists(request_form)
        if large_tags:
            tag_writer = PriceTag(tags_path=tags_path, fonts_path=fonts_path)
            countries = {
                region.name: region for region in mongo_db.get_items("countries")
            }
            tag_writer.write_large_tags(large_tags, shop.username, countries)
        if small_tags:
            tag_writer = PriceTag()
            tag_writer.write_small_tag(small_tags, shop.username)


def build_tag_lists(
    request_form: dict[str, Any],
) -> tuple[list[tuple[TagArticle, int]], list[tuple[TagArticle, int]]]:
    article_types = {
        article_type.name: article_type for article_type in mongo_db.get_types()
    }

    large_tags = []
    small_tags = []
    for article_id, number_of_tag in request_form.items():
        if number_of_tag == "":
            continue

        article = mongo_db.get_article_by_id(article_id)
        ratio_category = article_types[article.type].ratio_category
        tag_article = TagArticle(
            **article.model_dump(by_alias=True),
            ratio_category=ratio_category,
        )
        if ratio_category in large_tag_category:
            large_tags.append((tag_article, int(number_of_tag)))
        if ratio_category in small_tag_category:
            small_tags.append((tag_article, int(number_of_tag)))

    return large_tags, small_tags
