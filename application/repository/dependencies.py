from application.repository.client import database
from application.repository.mongodb import MongoRepository


class RepositoryProvider:
    def __call__(self) -> MongoRepository:
        return MongoRepository(database=database)


repository_provider = RepositoryProvider()
