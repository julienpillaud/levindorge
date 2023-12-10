from wizishop import WiziShopClient
from wizishop.entities.product import Product
from wizishop.entities.response import WiziShopResponse

from app.config import settings


class WizishopManager:
    @staticmethod
    def get_products() -> list[Product]:
        client = WiziShopClient(
            username=settings.WIZISHOP_EMAIL, password=settings.WIZISHOP_PASSWORD
        )
        products = client.get_products(limit=5000)
        return products.results

    @staticmethod
    def update_sku_stock(sku: str, stock: int) -> WiziShopResponse:
        client = WiziShopClient(
            username=settings.WIZISHOP_EMAIL, password=settings.WIZISHOP_PASSWORD
        )
        return client.update_sku_stock(sku=sku, stock=stock)
