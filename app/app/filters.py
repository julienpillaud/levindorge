import datetime
import json
from collections.abc import Callable
from zoneinfo import ZoneInfo

from app.data import navbar_categories
from app.domain.articles.entities import ArticleShop


def strip_zeros(value: float) -> str:
    return str(value).rstrip("0").rstrip(".")


def get_navbar_category_title(list_category: str) -> str:
    for _, categories in navbar_categories.items():
        for category in categories:
            if category.code == list_category:
                return category.plural_name
    return list_category


def create_local_timezone_filter(
    zone_info: ZoneInfo,
) -> Callable[[datetime.datetime], datetime.datetime]:
    def local_timezone(value: datetime.datetime) -> datetime.datetime:
        return value.replace(tzinfo=datetime.UTC).astimezone(tz=zone_info)

    return local_timezone


def article_shops_to_json(article_shops: dict[str, ArticleShop]) -> str:
    return json.dumps(
        {shop: shop_data.model_dump() for shop, shop_data in article_shops.items()}
    )
