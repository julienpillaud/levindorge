import pytest
from faker import Faker
from pymongo.database import Database

from app.infrastructure.repository.types import MongoDocument
from tests.factories.articles import ArticleFactory
from tests.factories.categories import CategoryFactory
from tests.factories.deposits import DepositFactory
from tests.factories.distributors import DistributorFactory
from tests.factories.origins import OriginFactory
from tests.factories.producers import ProducerFactory
from tests.factories.stores import StoreFactory
from tests.factories.volumes import VolumeFactory


@pytest.fixture
def faker() -> Faker:
    return Faker("fr_FR")


@pytest.fixture
def store_factory(faker: Faker, database: Database[MongoDocument]) -> StoreFactory:
    return StoreFactory(faker=faker, database=database)


@pytest.fixture
def category_factory(
    faker: Faker, database: Database[MongoDocument]
) -> CategoryFactory:
    return CategoryFactory(faker=faker, database=database)


@pytest.fixture
def article_factory(faker: Faker, database: Database[MongoDocument]) -> ArticleFactory:
    return ArticleFactory(faker=faker, database=database)


@pytest.fixture
def deposit_factory(faker: Faker, database: Database[MongoDocument]) -> DepositFactory:
    return DepositFactory(faker=faker, database=database)


@pytest.fixture
def distributor_factory(
    faker: Faker,
    database: Database[MongoDocument],
) -> DistributorFactory:
    return DistributorFactory(faker=faker, database=database)


@pytest.fixture
def origin_factory(faker: Faker, database: Database[MongoDocument]) -> OriginFactory:
    return OriginFactory(faker=faker, database=database)


@pytest.fixture
def producer_factory(
    faker: Faker,
    database: Database[MongoDocument],
) -> ProducerFactory:
    return ProducerFactory(faker=faker, database=database)


@pytest.fixture
def volume_factory(faker: Faker, database: Database[MongoDocument]) -> VolumeFactory:
    return VolumeFactory(faker=faker, database=database)
