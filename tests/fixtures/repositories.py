import pytest
from cleanstack.infrastructure.mongo.entities import MongoDocument
from pymongo.database import Database

from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.stores import StoreRepository
from app.infrastructure.repository.users import UserRepository


@pytest.fixture
def store_repository(database: Database[MongoDocument]) -> StoreRepository:
    return StoreRepository(database=database)


@pytest.fixture
def user_repository(database: Database[MongoDocument]) -> UserRepository:
    return UserRepository(database=database)


@pytest.fixture
def category_repository(database: Database[MongoDocument]) -> CategoryRepository:
    return CategoryRepository(database=database)


@pytest.fixture
def article_repository(database: Database[MongoDocument]) -> ArticleRepository:
    return ArticleRepository(database=database)
