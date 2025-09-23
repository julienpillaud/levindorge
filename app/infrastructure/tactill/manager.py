from tactill import TactillClient
from tactill.entities.catalog.article import Article as TactillArticle
from tactill.entities.catalog.article import ArticleCreation
from tactill.entities.catalog.category import Category
from tactill.entities.catalog.tax import Tax

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.shops.entities import Shop
from app.infrastructure.tactill.utils import define_color, define_icon_text, define_name


class TactillManagerError(Exception):
    pass


class TactillManager:
    def __init__(self, api_key: str) -> None:
        self.client = TactillClient(api_key=api_key)

    def get_category(self, name: str) -> Category:
        filter_ = f"deprecated=false&is_default=false&name={name}"
        categories = self.client.get_categories(filter=filter_)
        if not categories:
            raise TactillManagerError()

        return categories[0]

    def get_tax(self, tax_rate: float) -> Tax:
        filter_ = f"deprecated=false&tax_rate={tax_rate}"
        taxes = self.client.get_taxes(filter=filter_)
        if not taxes:
            raise TactillManagerError()

        return taxes[0]

    def create(
        self,
        article: Article,
        shop: Shop,
        category_name: str,
        display_group: DisplayGroup,
    ) -> TactillArticle:
        tactill_category = self.get_category(name=category_name)
        tactill_tax = self.get_tax(tax_rate=article.tax)

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(display_group=display_group, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(display_group=display_group, article=article),
            full_price=article.shops[shop.username].sell_price,
            barcode=article.barcode,
            reference=article.id,
            in_stock=True,
        )
        return self.client.create_article(article_creation=article_creation)
