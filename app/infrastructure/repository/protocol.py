from typing import Protocol

from pymongo.database import Database

from app.infrastructure.repository.mongo_repository import MongoDocument


class MongoRepositoryProtocol(Protocol):
    database: Database[MongoDocument]
