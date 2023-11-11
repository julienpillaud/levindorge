import math
from datetime import datetime, timezone

from application.blueprints.auth import Role, User
from application.entities.article import (
    Article,
    ArticleMargin,
    ArticleShops,
    AugmentedArticle,
    CreateOrUpdateArticle,
    RequestArticle,
    ExtendedArticle,
)
from application.entities.shop import Shop, ShopMargin
from application.interfaces.repository import IRepository


class ArticleManager:
    @staticmethod
    def get(repository: IRepository) -> list[ExtendedArticle]:
        return repository.get_extended_articles()

    @staticmethod
    def list(
        repository: IRepository, list_category: str, current_shop: Shop
    ) -> list[AugmentedArticle]:
        articles = repository.get_articles_by_list(list_category)
        ratio_category = repository.get_ratio_category(list_category)

        augmented_articles = []
        for article in articles:
            recommended_price = compute_recommended_price(
                taxfree_price=article.taxfree_price,
                tax=article.tax,
                shop_margins=current_shop.margins[ratio_category],
                ratio_category=ratio_category,
            )
            margin = compute_article_margin(
                taxfree_price=article.taxfree_price,
                tax=article.tax,
                sell_price=article.shops[current_shop.username].sell_price,
            )

            augmented_article = AugmentedArticle(
                **article.model_dump(by_alias=True),
                recommended_price=recommended_price,
                margin=margin,
            )
            augmented_articles.append(augmented_article)

        return augmented_articles

    @staticmethod
    def create(
        repository: IRepository,
        current_user: User,
        request_article: RequestArticle,
        article_shops: ArticleShops,
    ) -> Article:
        validated = current_user.role == Role.ADMIN
        date = datetime.now(timezone.utc)
        article_create = CreateOrUpdateArticle(
            validated=validated,
            created_by=current_user.name,
            created_at=date,
            updated_at=date,
            shops=article_shops,
            **request_article.model_dump(),
        )
        insert_result = repository.create_article(article_create)
        return repository.get_article_by_id(article_id=insert_result.inserted_id)

    @staticmethod
    def update(
        repository: IRepository,
        current_user: User,
        request_article: RequestArticle,
        article_shops: ArticleShops,
        article: Article,
    ) -> Article:
        validated = True if current_user.role == Role.ADMIN else article.validated
        date = datetime.now(timezone.utc)
        article_update = CreateOrUpdateArticle(
            validated=validated,
            created_by=article.created_by,
            created_at=article.created_at,
            updated_at=date,
            shops=article_shops,
            **request_article.model_dump(),
        )
        repository.update_article(article.id, article_update)
        return repository.get_article_by_id(article_id=article.id)

    @staticmethod
    def delete(repository: IRepository, article_id: str) -> None:
        repository.delete_article(article_id)


def compute_recommended_price(
    taxfree_price: float,
    tax: float,
    shop_margins: ShopMargin,
    ratio_category: str,
) -> float:
    ratio = shop_margins.ratio
    if ratio_category == "spirit" and taxfree_price >= 100:
        ratio += 10

    if shop_margins.operator == "+":
        price = (taxfree_price + ratio) * (1 + tax / 100)
    else:
        price = (taxfree_price * ratio) * (1 + tax / 100)

    if shop_margins.decimal_round < 0.1:
        return math.ceil(price * (1 / shop_margins.decimal_round)) / (
            1 / shop_margins.decimal_round
        )

    return round(price * (1 / shop_margins.decimal_round)) / (
        1 / shop_margins.decimal_round
    )


def compute_article_margin(
    taxfree_price: float, tax: float, sell_price: float
) -> ArticleMargin:
    margin = compute_margin(taxfree_price=taxfree_price, tax=tax, sell_price=sell_price)
    markup = compute_markup(tax=tax, sell_price=sell_price, margin=margin)
    return ArticleMargin(margin=round(margin, 2), markup=round(markup))


def compute_margin(taxfree_price: float, tax: float, sell_price: float) -> float:
    tax_factor = 1 + (tax / 100)
    return (sell_price / tax_factor) - taxfree_price


def compute_markup(tax: float, sell_price: float, margin: float) -> float:
    if sell_price == 0:
        return 0
    tax_factor = 1 + (tax / 100)
    return margin / (sell_price / tax_factor) * 100
