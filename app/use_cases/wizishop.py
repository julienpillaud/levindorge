from wizishop import WiziShopClient
from wizishop.entities.product import Product
from wizishop.entities.response import WiziShopResponse

from app.config import settings


class WiziShopManager:
    def __init__(self) -> None:
        self.client = WiziShopClient(
            username=settings.WIZISHOP_EMAIL, password=settings.WIZISHOP_PASSWORD
        )

    def get_products(self) -> list[Product]:
        products = self.client.get_products(limit=5000)
        return products.results

    def update_sku_stock(self, sku: str, stock: int) -> WiziShopResponse:
        return self.client.update_sku_stock(sku=sku, stock=stock)
