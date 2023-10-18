from tactill import TactillClient
from tactill.entities.catalog.article import Article as TactillArticle
from tactill.entities.catalog.article import ArticleCreation, ArticleModification
from tactill.entities.base import TactillColor, TactillResponse

from application.entities.article import Article, ArticleType
from application.entities.shop import Shop


class TactillManagerError(Exception):
    pass


class TactillManager:
    @staticmethod
    def create(
        shop: Shop,
        article: Article,
        article_type: ArticleType,
    ) -> TactillArticle:
        client = TactillClient(api_key=shop.tactill_api_key)

        tactill_categories = client.get_categories(
            filter=f"name={article_type.tactill_category}"
        )
        tactill_category = next(iter(tactill_categories), None)
        if not tactill_category:
            raise TactillManagerError("Category not found")

        tactill_taxes = client.get_taxes(filter=f"rate={article.tax}")
        tactill_tax = next(iter(tactill_taxes), None)
        if not tactill_tax:
            raise TactillManagerError("Tax not found")

        article_creation = ArticleCreation(
            category_id=tactill_category.id,
            taxes=[tactill_tax.id],
            name=define_name(list_category=article_type.list_category, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            full_price=article.shops[shop.username].sell_price,
            barcode=article.barcode,
            reference=article.id,
            in_stock=True,
        )
        return client.create_article(article_creation=article_creation)

    @staticmethod
    def update(
        shop: Shop,
        article: Article,
        article_type: ArticleType,
    ) -> TactillResponse:
        client = TactillClient(api_key=shop.tactill_api_key)

        tactill_articles = client.get_articles(filter=f"reference={article.id}")
        tactill_article = next(iter(tactill_articles), None)
        if not tactill_article:
            raise TactillManagerError("Article not found")

        article_modification = ArticleModification(
            taxes=tactill_article.taxes,
            name=define_name(list_category=article_type.list_category, article=article),
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            full_price=article.shops[shop.username].sell_price,
            barcode=article.barcode,
            in_stock=tactill_article.in_stock,
        )

        return client.update_article(
            article_id=tactill_article.id, article_modification=article_modification
        )

    @staticmethod
    def delete(shop: Shop, article_id: str) -> TactillResponse:
        client = TactillClient(api_key=shop.tactill_api_key)
        tactill_articles = client.get_articles(filter=f"reference={article_id}")

        if tactill_article := next(iter(tactill_articles), None):
            return client.delete_article(article_id=tactill_article.id)

        raise TactillManagerError("Article not found")


def format_volume(article: Article) -> str:
    if article.volume > 100:
        volume = str(article.volume / 100).rstrip("0").rstrip(".")
        unit = "L"
    else:
        volume = str(article.volume).rstrip("0").rstrip(".")
        unit = "cl"
    return f"{volume}{unit}"


def define_name(list_category: str, article: Article) -> str:
    name1 = article.name.name1
    name2 = article.name.name2
    volume = format_volume(article)
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
    if article.volume == 0:
        return "    "

    if article.volume > 100:
        return str(article.volume / 100).rstrip("0").rstrip(".").ljust(4)

    return str(article.volume).rstrip("0").rstrip(".").ljust(4)


def define_color(list_category: str, article: Article) -> TactillColor:
    if list_category in {"beer", "cider", "keg", "mini_keg"}:
        beer_colors = {
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
        wine_colors = {
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
