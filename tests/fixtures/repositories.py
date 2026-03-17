import pytest
from cleanstack.infrastructure.mongo.uow import MongoContext

from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.stores import StoreRepository


@pytest.fixture
def store_repository(mongo_context: MongoContext) -> StoreRepository:
    return StoreRepository(database=mongo_context.database)


@pytest.fixture
def category_repository(mongo_context: MongoContext) -> CategoryRepository:
    return CategoryRepository(database=mongo_context.database)


@pytest.fixture
def article_repository(mongo_context: MongoContext) -> ArticleRepository:
    return ArticleRepository(database=mongo_context.database)
