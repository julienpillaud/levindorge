from tactill import TactillClient
from tactill.entities.base import TactillColor, TactillResponse
from tactill.entities.catalog.article import Article as TactillArticle
from tactill.entities.catalog.article import ArticleCreation, ArticleModification
from tactill.entities.catalog.category import Category
from tactill.entities.catalog.tax import Tax
from tactill.entities.stock.movement import ArticleMovement, MovementCreation
from tactill.utils import get_query_filter

from app.entities.article import Article, ArticleType
from app.entities.shop import Shop


filter_prefix = "deprecated=false&is_default=false"
excluded_categories = ["AUTRE", "BAR", "CONSIGNE", "STREETFOOD", "VDO"]
categories_mapping = {
    "beer": ["BIÈRE", "CIDRE"],
    "keg": ["FÛT", "MINI-FÛT"],
    "spirit": [
        "ABSINTHE",
        "ANISÉ",
        "ARMAGNAC",
        "CACHAÇA",
        "COGNAC",
        "GIN",
        "LIQUEUR",
        "MEZCAL",
        "RHUM",
        "RHUM ARRANGÉ",
        "VODKA",
        "WHISKY",
    ],
    "wine": ["BIB", "VIN", "VIN EFFERVESCENT", "VIN MUTÉ"],
    "other": ["ACCESSOIRE", "ALIMENTATION", "BSA", "COFFRET", "EMBALLAGE"],
}


class TactillManagerError(Exception):
    pass


class TactillManager:
    def __init__(self, shop: Shop) -> None:
        self.shop = shop
        self.client = TactillClient(api_key=shop.tactill_api_key)

    def get(self) -> list[TactillArticle]:
        query_filter = get_query_filter(
            field="name", values=excluded_categories, query_operator="nin"
        )
        categories = self.client.get_categories(
            filter=f"{filter_prefix}&{query_filter}"
        )
        category_ids = [category.id for category in categories]

        query_filter = get_query_filter(
            field="category_id", values=category_ids, query_operator="in"
        )
        return self.client.get_articles(
            limit=5000, filter=f"{filter_prefix}&{query_filter}"
        )

    def get_category(self, article_type: ArticleType) -> Category:
        categories = self.client.get_categories(
            filter=f"{filter_prefix}&name={article_type.tactill_category}"
        )
        if category := next(iter(categories), None):
            return category

        raise TactillManagerError("Category not found")

    def get_tax(self, article: Article) -> Tax:
        taxes = self.client.get_taxes(filter=f"deprecated=false&rate={article.tax}")
        if tax := next(iter(taxes), None):
            return tax

        raise TactillManagerError("Tax not found")

    def create(
        self,
        article: Article,
        article_type: ArticleType,
    ) -> TactillArticle:
        tactill_category = self.get_category(article_type=article_type)
        tactill_tax = self.get_tax(article=article)

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(list_category=article_type.list_category, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            full_price=article.shops[self.shop.username].sell_price,
            barcode=article.barcode,
            reference=article.id,
            in_stock=True,
        )
        return self.client.create_article(article_creation=article_creation)

    def update_or_create(
        self,
        article: Article,
        article_type: ArticleType,
    ) -> TactillResponse | TactillArticle:
        tactill_articles = self.client.get_articles(
            filter=f"{filter_prefix}&reference={article.id}"
        )
        tactill_article = next(iter(tactill_articles), None)
        if not tactill_article:
            return self.create(article=article, article_type=article_type)

        tactill_category = self.get_category(article_type=article_type)
        tactill_tax = self.get_tax(article=article)

        article_modification = ArticleModification(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(list_category=article_type.list_category, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            full_price=article.shops[self.shop.username].sell_price,
            barcode=article.barcode,
            in_stock=True,
        )

        return self.client.update_article(
            article_id=tactill_article.id, article_modification=article_modification
        )

    def delete_by_id(self, article_id: str) -> TactillResponse:
        if tactill_article := self.client.get_article(article_id=article_id):
            return self.client.delete_article(article_id=tactill_article.id)
        raise TactillManagerError("Article not found")

    def delete_by_reference(self, article_id: str) -> TactillResponse:
        tactill_articles = self.client.get_articles(
            filter=f"{filter_prefix}&reference={article_id}"
        )

        if tactill_article := next(iter(tactill_articles), None):
            return self.client.delete_article(article_id=tactill_article.id)

        raise TactillManagerError("Article not found")

    def reset_stock(self, request_category: str):
        category_names = categories_mapping.get(request_category)
        if not category_names:
            raise TactillManagerError("Request category not found")

        query_filter = get_query_filter(
            field="name", values=category_names, query_operator="in"
        )
        categories = self.client.get_categories(
            filter=f"{filter_prefix}&{query_filter}"
        )
        category_mapping = {category.id: category.name for category in categories}

        query_filter = get_query_filter(
            field="category_id",
            values=list(category_mapping.keys()),
            query_operator="in",
        )
        articles = self.client.get_articles(
            limit=5000, filter=f"{filter_prefix}&{query_filter}"
        )

        article_movements_out = []
        article_movements_in = []
        for article in articles:
            if article.stock_quantity > 0:
                article_movements_out.append(
                    ArticleMovement(
                        article_id=article.id,
                        article_name=article.name,
                        category_name=category_mapping[article.category_id],
                        state="done",
                        units=article.stock_quantity,
                    )
                )
            if article.stock_quantity < 0:
                article_movements_in.append(
                    ArticleMovement(
                        article_id=article.id,
                        article_name=article.name,
                        category_name=category_mapping[article.category_id],
                        state="done",
                        units=-article.stock_quantity,
                    )
                )

        if article_movements_out:
            movement_creation_out = MovementCreation(
                validated_by=[],
                type="out",
                state="done",
                movements=article_movements_out,
            )
            self.client.create_movement(movement_creation=movement_creation_out)

        if article_movements_in:
            movement_creation_in = MovementCreation(
                validated_by=[],
                type="in",
                state="done",
                movements=article_movements_in,
            )
            self.client.create_movement(movement_creation=movement_creation_in)


def format_volume(article: Article) -> str:
    if not article.volume:
        return ""

    volume = article.volume.value
    unit = article.volume.unit
    if article.volume.unit == "cL" and article.volume.value > 100:
        volume = article.volume.value / 100
        unit = "L"

    volume_str = str(volume).rstrip("0").rstrip(".")
    return f"{volume_str}{unit}"


def define_name(list_category: str, article: Article) -> str:
    name1 = article.name.name1
    name2 = article.name.name2
    volume = format_volume(article=article)
    color = article.color

    if list_category in {"beer", "cider"}:
        return f"{name2} {volume} {name1}".strip()

    if list_category in {"keg", "mini_keg"}:
        return f"{name1} {name2} {volume}" if name1 else f"{name2} {volume}"

    if list_category in {"rhum", "whisky", "spirit", "arranged", "sparkling_wine"}:
        return f"{name1} {name2} {volume}" if name1 else f"{name2} {volume}"

    if list_category in {"bib", "wine", "fortified_wine"}:
        if not name1:
            return f"{name2} {color} {volume}"

        if name2:
            return f"{name2} {color} {volume} {name1}"
        else:
            return f"{name1} {color} {volume}"

    if list_category in {"box", "misc", "food"}:
        return f"{name1}"

    raise ValueError


def define_icon_text(article: Article) -> str:
    if not article.volume:
        return "    "

    volume = article.volume.value
    if article.volume.unit == "cL" and article.volume.value > 100:
        volume = article.volume.value / 100

    return str(volume).rstrip("0").rstrip(".").ljust(4)


def define_color(list_category: str, article: Article) -> TactillColor:
    if list_category in {"beer", "cider", "keg", "mini_keg"}:
        beer_colors: dict[str, TactillColor] = {
            "Ambrée": "#FF6347",
            "Blanche": "#9EA09E",
            "Blonde": "#F2BA43",
            "Brune": "#A06E58",
            "Fruitée": "#F44F60",
        }
        return beer_colors.get(article.color, "#9EA09E")

    if list_category == "rhum":
        return "#30BEA5"

    if list_category == "whisky":
        return "#1E8CFF"

    if list_category in {"spirit", "arranged"}:
        return "#9EA09E"

    if list_category in {"wine", "fortified_wine", "sparkling_wine", "bib"}:
        wine_colors: dict[str, TactillColor] = {
            "Blanc": "#F2BA43",
            "Rosé": "#B455C8",
            "Rouge": "#F44F60",
        }
        return wine_colors.get(article.color, "#9EA09E")

    if list_category == "box":
        return "#B455C8"

    if list_category in {"misc", "food"}:
        return "#57DB47"

    raise ValueError
