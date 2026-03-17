import pytest
from cleanstack.infrastructure.mongo.uow import MongoContext
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
def store_factory(faker: Faker, mongo_context: MongoContext) -> StoreFactory:
    return StoreFactory(faker=faker, context=mongo_context)


@pytest.fixture
def category_factory(faker: Faker, mongo_context: MongoContext) -> CategoryFactory:
    return CategoryFactory(faker=faker, context=mongo_context)


@pytest.fixture
def article_factory(faker: Faker, mongo_context: MongoContext) -> ArticleFactory:
    return ArticleFactory(faker=faker, context=mongo_context)


@pytest.fixture
def deposit_factory(faker: Faker, mongo_context: MongoContext) -> DepositFactory:
    return DepositFactory(faker=faker, context=mongo_context)


@pytest.fixture
def distributor_factory(
    faker: Faker, mongo_context: MongoContext
) -> DistributorFactory:
    return DistributorFactory(faker=faker, context=mongo_context)


@pytest.fixture
def origin_factory(faker: Faker, mongo_context: MongoContext) -> OriginFactory:
    return OriginFactory(faker=faker, context=mongo_context)


@pytest.fixture
def producer_factory(faker: Faker, mongo_context: MongoContext) -> ProducerFactory:
    return ProducerFactory(faker=faker, context=mongo_context)


@pytest.fixture
def volume_factory(faker: Faker, mongo_context: MongoContext) -> VolumeFactory:
    return VolumeFactory(faker=faker, context=mongo_context)
