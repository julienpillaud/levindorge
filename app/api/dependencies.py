from functools import lru_cache
from typing import cast

from fastapi.requests import Request

from app.core.config import Settings
from app.domain.domain import Domain


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_domain(request: Request) -> Domain:
    return cast(Domain, request.app.state.domain)
