from cleanstack.infrastructure.mongodb.uow import MongoDBContext

from app.core.config.settings import Settings
from app.core.context import Context


def get_context(settings: Settings) -> Context:
    mongo_context = MongoDBContext.from_settings(
        host=settings.mongo_uri,
        database_name=settings.mongo_database,
    )
    return Context(settings=settings, mongo_context=mongo_context)
