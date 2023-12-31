import re

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from tactill import TactillError
from wizishop import WiziShopError

from app.config import settings
from app.entities.article import ExtendedArticle
from app.entities.shop import Shop
from app.use_cases.articles import ArticleManager
from app.use_cases.tactill import TactillManager, TactillManagerError
from app.repository.dependencies import repository_provider
from app.use_cases.wizishop import WiziShopManager

celery_app = Celery(
    "worker", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
celery_app.conf.timezone = "Europe/Paris"

logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    if settings.ENVIRONMENT == "production":
        sender.add_periodic_task(
            crontab(
                minute="*/30",
                hour="11-23",
                day_of_week="1-6",
            ),
            task_update_dashboard_stocks.s(),
            name="update dashboard stocks",
        )
        sender.add_periodic_task(
            crontab(
                minute="*/30",
                hour="11-23",
                day_of_week="1-6",
            ),
            task_update_wizishop_stocks.s(),
            name="update wizishop stocks",
        )
        sender.add_periodic_task(
            crontab(
                minute="0",
                hour="18",
                day_of_week="1-6",
            ),
            clean_tactill_articles.s(),
            name="clean tactill articles",
        )


@celery_app.task
def do_nothing() -> str:
    return "OK"


@celery_app.task(autoretry_for=(TactillError,), retry_backoff=True)
def task_update_dashboard_stocks() -> None:
    repository = repository_provider()

    shops = repository.get_shops()
    articles = ArticleManager.get(repository=repository)

    for shop in shops:
        tactill_stocks = get_tactill_stocks(shop=shop)
        dashboard_stocks = get_dashboard_stocks(shop=shop, articles=articles)
        update_dashboard_stocks(
            repository=repository,
            shop=shop,
            dashboard_stocks=dashboard_stocks,
            tactill_stocks=tactill_stocks,
        )


@celery_app.task(autoretry_for=(TactillError, WiziShopError), retry_backoff=True)
def task_update_wizishop_stocks() -> None:
    repository = repository_provider()
    client = WiziShopManager()

    shop = repository.get_shop_by_username("pessac")
    tactill_stocks = get_tactill_stocks(shop=shop)
    wizishop_stocks = get_wizishop_stocks(client=client)

    update_wizishop_stocks(
        client=client, wizishop_stocks=wizishop_stocks, tactill_stocks=tactill_stocks
    )


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def create_tactill_articles(article_id: str) -> None:
    repository = repository_provider()

    shops = repository.get_shops()
    article = repository.get_article_by_id(article_id=article_id)
    article_type = repository.get_article_type(article.type)

    for shop in shops:
        manager = TactillManager(shop=shop)
        manager.create(
            article=article,
            article_type=article_type,
        )


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def update_tactill_articles(article_id: str) -> None:
    repository = repository_provider()

    shops = repository.get_shops()
    article = repository.get_article_by_id(article_id=article_id)
    article_type = repository.get_article_type(article.type)

    for shop in shops:
        manager = TactillManager(shop=shop)
        manager.update_or_create(
            article=article,
            article_type=article_type,
        )


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def delete_tactill_articles(article_id: str) -> None:
    repository = repository_provider()

    shops = repository.get_shops()
    for shop in shops:
        manager = TactillManager(shop=shop)
        manager.delete_by_reference(article_id=article_id)


@celery_app.task(autoretry_for=(TactillError, TactillManagerError), retry_backoff=True)
def clean_tactill_articles() -> None:
    repository = repository_provider()

    shops = repository.get_shops()
    for shop in shops:
        manager = TactillManager(shop=shop)
        articles = manager.get()
        bad_articles = [article for article in articles if not article.reference]
        logger.info(f"{shop.name} clean : {bad_articles}")
        for article in bad_articles:
            manager.delete_by_id(article_id=article.id)


def get_tactill_stocks(shop: Shop) -> dict[str, int]:
    manager = TactillManager(shop=shop)
    articles = manager.get()
    return {article.reference: article.stock_quantity for article in articles}


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
    logger.info(f"{shop.name} dashboard : {stocks_to_update}")

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
    logger.info(f"WiziShop : {stocks_to_update}")

    for article_id, stock_quantity in stocks_to_update.items():
        client.update_sku_stock(sku=article_id, stock=stock_quantity)
