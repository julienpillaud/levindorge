from app.core.config import Settings
from app.domain.domain import TransactionalContextProtocol
from app.infrastructure.mongo_uow import MongoUnitOfWork


class Context(MongoUnitOfWork, TransactionalContextProtocol):
    def __init__(self, settings: Settings):
        super().__init__(settings)
