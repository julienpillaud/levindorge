from functools import lru_cache
from typing import Annotated

from fast_depends import Depends

from app.core.config.settings import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.domain import Domain
from app.infrastructure.repository.uow import MongoUnitOfWork


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_mongo_uow(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoUnitOfWork:
    return MongoUnitOfWork(settings=settings)


def get_uow(
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
) -> UnitOfWork:
    return UnitOfWork(mongo=mongo_uow)


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> Context:
    return Context(settings=settings, uow=uow)


def get_domain(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    context: Annotated[Context, Depends(get_context)],
) -> Domain:
    return Domain(uow=uow, context=context)
