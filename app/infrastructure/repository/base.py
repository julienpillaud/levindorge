from pymongo.database import Database

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.deposits import DepositRepository
from app.infrastructure.repository.inventories import InventoryRepository
from app.infrastructure.repository.mongo_repository import MongoDocument
from app.infrastructure.repository.types import ArticleTypeRepository


class MongoRepository(
    RepositoryProtocol,
    ArticleTypeRepository,
    DepositRepository,
    InventoryRepository,
):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database
