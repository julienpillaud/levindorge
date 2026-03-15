import pytest
from cleanstack.infrastructure.mongodb.uow import MongoDBContext

from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.stores import StoreRepository
from app.infrastructure.repository.users import UserRepository


@pytest.fixture
def store_repository(mongo_context: MongoDBContext) -> StoreRepository:
    return StoreRepository(database=mongo_context.database)


@pytest.fixture
def user_repository(mongo_context: MongoDBContext) -> UserRepository:
    return UserRepository(database=mongo_context.database)


@pytest.fixture
def category_repository(mongo_context: MongoDBContext) -> CategoryRepository:
    return CategoryRepository(database=mongo_context.database)


@pytest.fixture
def article_repository(mongo_context: MongoDBContext) -> ArticleRepository:
    return ArticleRepository(database=mongo_context.database)
