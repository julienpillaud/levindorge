from app.core.config.settings import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.infrastructure.repository.uow import MongoUnitOfWork


def get_context(settings: Settings) -> Context:
    mongo_uow = MongoUnitOfWork(settings=settings)
    uow = UnitOfWork(mongo=mongo_uow)
    return Context(settings=settings, uow=uow)
