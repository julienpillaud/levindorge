from application.entities.article import Article, ArticleType
from application.entities.shop import Shop
from utils.tactill import Tactill


class TactillManager:
    @staticmethod
    def create(
        shop: Shop,
        article: Article,
        article_type: ArticleType,
    ):
        api_key = shop.tactill_api_key
        session = Tactill(api_key=api_key)
        return session.create_article(
            category=article_type.tactill_category,
            tax_rate=article.tax,
            name=define_name(list_category=article_type.list_category, article=article),
            full_price=article.shops[shop.username].sell_price,
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            barcode=article.barcode,
            reference=article.id,
            in_stock="true",
        )

    @staticmethod
    def update(
        shop: Shop,
        article: Article,
        article_type: ArticleType,
    ):
        api_key = shop.tactill_api_key
        session = Tactill(api_key=api_key)
        return session.update_article(
            reference=article.id,
            name=define_name(list_category=article_type.list_category, article=article),
            full_price=article.shops[shop.username].sell_price,
            icon_text=define_icon_text(article=article),
            color=define_color(
                list_category=article_type.list_category, article=article
            ),
            barcode=article.barcode,
        )

    @staticmethod
    def delete(shop: Shop, article_id: str):
        api_key = shop.tactill_api_key
        session = Tactill(api_key=api_key)
        return session.delete_article(reference=article_id)


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

    elif list_category in {"box", "misc", "food"}:
        return f"{name1}"


def define_icon_text(article: Article) -> str:
    if article.volume == 0:
        return "    "

    if article.volume > 100:
        return str(article.volume / 100).rstrip("0").rstrip(".").ljust(4)

    return str(article.volume).rstrip("0").rstrip(".").ljust(4)


def define_color(list_category: str, article: Article) -> str:
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
