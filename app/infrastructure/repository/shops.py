from app.domain.protocols.repository import ShopRepositoryProtocol
from app.domain.shops.entities import Shop


class ShopRepository(ShopRepositoryProtocol):
    def get_shops(self) -> list[Shop]:
        return [Shop(**shop) for shop in self.database["shops"].find()]
