from functools import lru_cache
from typing import Any

import httpx

from app.domain.metadata.entities.origins import ArticleOrigin, OriginType


def get_origin(value: Any) -> ArticleOrigin | None:
    if not value:
        return None

    codes = fetch_codes()
    code = codes.get(value)
    if code:
        return ArticleOrigin(name=value, code=code, type=OriginType.COUNTRY)

    return ArticleOrigin(name=value, code=None, type=OriginType.REGION)


@lru_cache(maxsize=1)
def fetch_codes() -> dict[str, str]:
    response = httpx.get("https://flagcdn.com/fr/codes.json")
    return {v: k for k, v in response.json().items()}
