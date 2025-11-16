from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.api.utils import init_templates
from app.core.config import Settings
from app.domain.domain import Domain


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_domain(request: Request) -> Domain:
    return cast(Domain, request.app.state.domain)


@lru_cache(maxsize=1)
def get_templates(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Jinja2Templates:
    return init_templates(settings=settings)
