from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.core.context import Context
from app.domain.context import ContextProtocol
from app.domain.domain import Domain


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ContextProtocol:
    return Context(settings=settings)


def get_domain(
    context: Annotated[ContextProtocol, Depends(get_context)],
) -> Domain:
    return Domain(context=context)
