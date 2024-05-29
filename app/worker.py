import re

import logfire
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from tactill import TactillError
from tactill.entities.base import TactillResponse
from tactill.entities.catalog.article import Article as TactillArticle
from wizishop import WiziShopError

from app.config import settings
from app.entities.article import ExtendedArticle
from app.entities.shop import Shop
from app.repository.dependencies import repository_provider
from app.use_cases.articles import ArticleManager
from app.use_cases.tactill import (
    TactillManager,
    TactillManagerError,
    define_color,
    define_icon_text,
    define_name,
)
from app.use_cases.wizishop import WiziShopManager

logfire.configure()


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs):
    CeleryInstrumentor().instrument()


celery_app = Celery(
    "worker", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
celery_app.conf.timezone = "Europe/Paris"


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    if settings.ENVIRONMENT == "production":
        sender.add_periodic_task(
            crontab(
                minute="*/30",
                hour="11-23",
                day_of_week="1-6",
            ),
            update_stocks.s(),
        )
        sender.add_periodic_task(
            crontab(
                minute="0",
                hour="2",
                day_of_week="1-6",
            ),
            clean_tactill.s(),
        )
        sender.add_periodic_task(
            crontab(
                minute="0",
                hour="3",
                day_of_week="1-6",
            ),
            update_tactill.s(),
        )


@celery_app.task
def update_stocks() -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        update_shop_stocks.delay(shop.username)


@celery_app.task(
    autoretry_for=(TactillError, TactillManagerError, WiziShopError), retry_backoff=True
)
def update_shop_stocks(shop_username: str) -> None:
    repository = repository_provider()

    shop = repository.get_shop_by_username(username=shop_username)
    articles = ArticleManager.get(repository=repository)

    tactill_stocks = get_tactill_stocks(shop=shop)
    dashboard_stocks = get_dashboard_stocks(shop=shop, articles=articles)

    update_dashboard_stocks(
        repository=repository,
        shop=shop,
        dashboard_stocks=dashboard_stocks,
        tactill_stocks=tactill_stocks,
    )

    if shop.username == "pessac":
        client = WiziShopManager()
        wizishop_stocks = get_wizishop_stocks(client=client)
        update_wizishop_stocks(
            client=client,
            wizishop_stocks=wizishop_stocks,
            tactill_stocks=tactill_stocks,
        )


@celery_app.task
def create_tactill_articles(article_id: str) -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        create_tactill_article.delay(shop.username, article_id)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def create_tactill_article(shop_username: str, article_id: str) -> None:
    repository = repository_provider()

    shop = repository.get_shop_by_username(username=shop_username)
    article = repository.get_article_by_id(article_id=article_id)
    article_type = repository.get_article_type(article.type)

    manager = TactillManager(shop=shop)
    created_article = manager.create(
        article=article,
        article_type=article_type,
    )
    logfire.info(f"{shop.name}: {created_article.name} - article successfully created")


@celery_app.task
def update_tactill_articles(article_id: str) -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        update_tactill_article.delay(shop.username, article_id)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def update_tactill_article(shop_username: str, article_id: str) -> None:
    repository = repository_provider()

    shop = repository.get_shop_by_username(username=shop_username)
    article = repository.get_article_by_id(article_id=article_id)
    article_type = repository.get_article_type(article.type)

    manager = TactillManager(shop=shop)
    result = manager.update_or_create(
        article=article,
        article_type=article_type,
    )

    if isinstance(result, TactillResponse):
        tactill_name = define_name(
            list_category=article_type.list_category, article=article
        )
        logfire.info(f"{shop.name}: {tactill_name} - {result.message}")
    if isinstance(result, TactillArticle):
        logfire.info(f"{shop.name}: {result.name} - article successfully created")


@celery_app.task
def delete_tactill_articles(article_id: str) -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        delete_tactill_article_by_reference.delay(shop.username, article_id)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def delete_tactill_article_by_reference(shop_username: str, article_id: str) -> None:
    repository = repository_provider()
    shop = repository.get_shop_by_username(username=shop_username)

    manager = TactillManager(shop=shop)
    result = manager.delete_by_reference(reference=article_id)

    logfire.info(f"{shop.name} - {result.message}")


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def delete_tactill_article_by_id(shop_username: str, article_id: str) -> None:
    repository = repository_provider()
    shop = repository.get_shop_by_username(username=shop_username)

    manager = TactillManager(shop=shop)
    result = manager.delete_by_id(article_id=article_id)

    logfire.info(f"{shop.name} - {result.message}")


# ==============================================================================
# 1. Delete articles in managed categories but without reference
@celery_app.task
def clean_tactill() -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        clean_tactill_shop.delay(shop.username)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def clean_tactill_shop(shop_username: str) -> None:
    repository = repository_provider()
    shop = repository.get_shop_by_username(username=shop_username)

    manager = TactillManager(shop=shop)
    tactill_articles = manager.get()
    bad_articles = [article for article in tactill_articles if not article.reference]
    if not bad_articles:
        logfire.info(f"{shop.name}: no article to clean")
    for article in bad_articles:
        delete_tactill_article_by_id.delay(shop.username, article.id)


# ==============================================================================
# 2. Create missing articles and update articles with wrong values
@celery_app.task
def update_tactill() -> None:
    repository = repository_provider()
    for shop in repository.get_shops():
        update_tactill_shop.delay(shop.username)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def update_tactill_shop(shop_username: str) -> None:
    repository = repository_provider()
    articles = ArticleManager.get(repository=repository)
    shop = repository.get_shop_by_username(username=shop_username)

    manager = TactillManager(shop=shop)
    tactill_articles = manager.get()
    tactill_articles_mapping = {
        article.reference: article for article in tactill_articles
    }
    category_mapping = get_category_mapping(manager)
    tax_mapping = get_tax_mapping(manager)

    updated = []
    for article in articles:
        tactill_article = tactill_articles_mapping.get(article.id)
        if not tactill_article:
            updated.append(article.id)
            create_tactill_article.delay(shop.username, article.id)
            continue

        if not check_articles(
            article, tactill_article, shop, category_mapping, tax_mapping
        ):
            updated.append(article.id)
            update_tactill_article.delay(shop.username, article.id)

    if not updated:
        logfire.info(f"{shop.name}: no article to update")


# ==============================================================================
def get_tactill_stocks(shop: Shop) -> dict[str, int]:
    manager = TactillManager(shop=shop)
    articles = manager.get()
    return {article.reference: article.stock_quantity for article in articles}


def get_tax_mapping(manager: TactillManager) -> dict[float, str]:
    return {tax.rate: tax.id for tax in manager.get_taxes()}


def get_category_mapping(manager: TactillManager) -> dict[str, str]:
    return {category.name: category.id for category in manager.get_categories()}


def check_articles(
    article: ExtendedArticle,
    tactill_article: TactillArticle,
    shop: Shop,
    category_mapping: dict[str, str],
    taxes_mapping: dict[float, str],
) -> bool:
    category_id = category_mapping[article.article_type.tactill_category]
    tax_id = taxes_mapping[article.tax]
    name = define_name(article.article_type.list_category, article)
    icon_text = define_icon_text(article)
    color = define_color(article.article_type.list_category, article)
    return (
        category_id == tactill_article.category_id
        and [tax_id] == tactill_article.taxes
        and name == tactill_article.name
        and icon_text == tactill_article.icon_text
        and color == tactill_article.color
        and article.shops[shop.username].sell_price == tactill_article.full_price
        and article.barcode == tactill_article.barcode
    )


def get_dashboard_stocks(shop: Shop, articles: list[ExtendedArticle]) -> dict[str, int]:
    return {
        article.id: article.shops[shop.username].stock_quantity for article in articles
    }


def update_dashboard_stocks(
    repository,
    shop: Shop,
    dashboard_stocks: dict[str, int],
    tactill_stocks: dict[str, int],
) -> None:
    stocks_to_update = {}
    for article_id, dashboard_stock in dashboard_stocks.items():
        tactill_stock = tactill_stocks.get(article_id)
        if tactill_stock is not None and tactill_stock != dashboard_stock:
            stocks_to_update[article_id] = tactill_stock
    logfire.info(f"{shop.name} updated : {stocks_to_update}")

    for article_id, stock_quantity in stocks_to_update.items():
        repository.update_article_stock_quantity(
            article_id=article_id, stock_quantity=stock_quantity, shop=shop
        )


def get_wizishop_stocks(client: WiziShopManager) -> dict[str, int]:
    articles = client.get_products()

    return {
        article.sku: article.stock
        for article in articles
        if re.match("^[0-9A-Fa-f]{24}$", article.sku) and article.stock is not None
    }


def update_wizishop_stocks(
    client: WiziShopManager,
    wizishop_stocks: dict[str, int],
    tactill_stocks: dict[str, int],
) -> None:
    stocks_to_update = {}
    for article_id, wizishop_stock in wizishop_stocks.items():
        tactill_stock = tactill_stocks.get(article_id)
        if tactill_stock is not None and tactill_stock != wizishop_stock:
            stocks_to_update[article_id] = tactill_stock
    logfire.info(f"Pessac WiziShop : {stocks_to_update}")

    for article_id, stock_quantity in stocks_to_update.items():
        client.update_sku_stock(sku=article_id, stock=stock_quantity)
