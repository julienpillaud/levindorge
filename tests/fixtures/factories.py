import pytest
from cleanstack.infrastructure.mongodb.uow import MongoDBContext
from faker import Faker

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
def store_factory(faker: Faker, mongo_context: MongoDBContext) -> StoreFactory:
    return StoreFactory(faker=faker, context=mongo_context)


@pytest.fixture
def category_factory(faker: Faker, mongo_context: MongoDBContext) -> CategoryFactory:
    return CategoryFactory(faker=faker, context=mongo_context)


@pytest.fixture
def article_factory(faker: Faker, mongo_context: MongoDBContext) -> ArticleFactory:
    return ArticleFactory(faker=faker, context=mongo_context)


@pytest.fixture
def deposit_factory(faker: Faker, mongo_context: MongoDBContext) -> DepositFactory:
    return DepositFactory(faker=faker, context=mongo_context)


@pytest.fixture
def distributor_factory(
    faker: Faker, mongo_context: MongoDBContext
) -> DistributorFactory:
    return DistributorFactory(faker=faker, context=mongo_context)


@pytest.fixture
def origin_factory(faker: Faker, mongo_context: MongoDBContext) -> OriginFactory:
    return OriginFactory(faker=faker, context=mongo_context)


@pytest.fixture
def producer_factory(faker: Faker, mongo_context: MongoDBContext) -> ProducerFactory:
    return ProducerFactory(faker=faker, context=mongo_context)


@pytest.fixture
def volume_factory(faker: Faker, mongo_context: MongoDBContext) -> VolumeFactory:
    return VolumeFactory(faker=faker, context=mongo_context)
