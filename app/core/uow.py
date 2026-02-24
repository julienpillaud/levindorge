from cleanstack.uow import CompositeUniOfWork

from app.infrastructure.repository.uow import MongoUnitOfWork


class UnitOfWork(CompositeUniOfWork):
    def __init__(self, mongo: MongoUnitOfWork) -> None:
        self.mongo = mongo
        super().__init__([self.mongo])
