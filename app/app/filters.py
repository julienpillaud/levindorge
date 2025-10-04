import datetime
from collections.abc import Callable
from typing import Any
from zoneinfo import ZoneInfo

from fastapi.requests import Request

from app.data import navbar_categories


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


def get_flashed_messages(request: Request) -> Any:
    return request.session.pop("_messages", [])
