from app.repository.client import get_database
from app.repository.mongodb import MongoRepository


class RepositoryProvider:
    def __call__(self) -> MongoRepository:
        database = get_database()
        return MongoRepository(database=database)


repository_provider = RepositoryProvider()
