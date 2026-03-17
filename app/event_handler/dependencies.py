from functools import lru_cache
from typing import Annotated

from cleanstack.domain import CompositeUniOfWork
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from fast_depends import Depends

from app.core.config.settings import Settings
from app.core.context import Context
from app.domain.domain import Domain


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_mongo_context(
    settings: Annotated[Settings, Depends(get_settings)],
) -> MongoContext:
    return MongoContext.from_settings(
        host=settings.mongo_uri,
        database_name=settings.mongo_database,
    )


def get_mongo_uow(
    context: Annotated[MongoContext, Depends(get_mongo_context)],
) -> MongoUnitOfWork:
    return MongoUnitOfWork(context=context)


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    mongo_context: Annotated[MongoContext, Depends(get_mongo_context)],
    mongo_uow: Annotated[MongoUnitOfWork, Depends(get_mongo_uow)],
) -> Context:
    return Context(
        settings=settings,
        mongo_context=mongo_context,
        mongo_uow=mongo_uow,
    )


def get_domain(context: Annotated[Context, Depends(get_context)]) -> Domain:
    uow = CompositeUniOfWork(members=context.members)
    return Domain(uow=uow, context=context)
