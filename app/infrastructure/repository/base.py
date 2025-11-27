from pymongo.database import Database

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.inventories import InventoryRepository
from app.infrastructure.repository.mongo_repository import MongoDocument


class MongoRepository(RepositoryProtocol, InventoryRepository):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database
