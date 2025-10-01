from app.domain.protocols.repository import ShopRepositoryProtocol
from app.domain.shops.entities import Shop
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class ShopRepository(MongoRepositoryProtocol, ShopRepositoryProtocol):
    def get_shops(self) -> list[Shop]:
        return [Shop(**shop) for shop in self.database["shops"].find()]
