from typing import Protocol

from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database


class MongoRepositoryProtocol(Protocol):
    database: Database[MongoDocument]
