import pytest
from pymongo.database import Database

from app.infrastructure.repository.base import MongoDocument
from tests.factories.articles import ArticleFactory
from tests.factories.categories import CategoryFactory
from tests.factories.stores import StoreFactory
from tests.factories.users import UserFactory


@pytest.fixture
def store_factory(database: Database[MongoDocument]) -> StoreFactory:
    return StoreFactory(database=database)


@pytest.fixture
def user_factory(database: Database[MongoDocument]) -> UserFactory:
    return UserFactory(database=database)


@pytest.fixture
def category_factory(database: Database[MongoDocument]) -> CategoryFactory:
    return CategoryFactory(database=database)


@pytest.fixture
def article_factory(database: Database[MongoDocument]) -> ArticleFactory:
    return ArticleFactory(database=database)
