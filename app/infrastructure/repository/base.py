from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.domain.protocols.repository import RepositoryProtocol
from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.items import ItemRepository
from app.infrastructure.repository.shops import ShopRepository
from app.infrastructure.repository.types import ArticleTypeRepository
from app.infrastructure.repository.users import UserRepository


class MongoRepository(
    RepositoryProtocol,
    ShopRepository,
    UserRepository,
    ArticleTypeRepository,
    ArticleRepository,
    ItemRepository,
):
    def __init__(self, database: Database[MongoDocument]):
        self.database = database
