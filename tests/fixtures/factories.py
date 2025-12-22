import pytest
from pymongo.database import Database

from app.infrastructure.repository.base import MongoDocument
from tests.factories.articles import ArticleFactory
from tests.factories.categories import CategoryFactory
from tests.factories.deposits import DepositFactory
from tests.factories.distributors import DistributorFactory
from tests.factories.origins import OriginFactory
from tests.factories.producers import ProducerFactory
from tests.factories.stores import StoreFactory
from tests.factories.users import UserFactory
from tests.factories.volumes import VolumeFactory


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


@pytest.fixture
def deposit_factory(database: Database[MongoDocument]) -> DepositFactory:
    return DepositFactory(database=database)


@pytest.fixture
def distributor_factory(database: Database[MongoDocument]) -> DistributorFactory:
    return DistributorFactory(database=database)


@pytest.fixture
def origin_factory(database: Database[MongoDocument]) -> OriginFactory:
    return OriginFactory(database=database)


@pytest.fixture
def producer_factory(database: Database[MongoDocument]) -> ProducerFactory:
    return ProducerFactory(database=database)


@pytest.fixture
def volume_factory(database: Database[MongoDocument]) -> VolumeFactory:
    return VolumeFactory(database=database)
