import random
import uuid
from typing import Any

from faker import Faker

from app.domain.articles.entities import (
    Article,
    ArticleColor,
    ArticleDeposit,
    ArticleMargins,
    ArticleStoreData,
    ArticleTaste,
    ArticleVolume,
)
from app.domain.stores.entities import Store
from app.infrastructure.repository.articles import ArticleRepository
from tests.factories.base import BaseMongoFactory
from tests.factories.categories import CategoryFactory
from tests.factories.deposits import DepositFactory
from tests.factories.distributors import DistributorFactory
from tests.factories.origins import OriginFactory
from tests.factories.producers import ProducerFactory
from tests.factories.utils import generate_decimal
from tests.factories.volumes import VolumeFactory


def generate_article_store_data() -> ArticleStoreData:
    return ArticleStoreData(
        gross_price=generate_decimal(decimal_places=2),
        bar_price=generate_decimal(decimal_places=2),
        stock_quantity=random.randint(0, 1000),
        recommended_price=generate_decimal(decimal_places=2),
        margins=ArticleMargins(
            margin_amount=generate_decimal(decimal_places=2),
            margin_rate=generate_decimal(decimal_places=0),
        ),
    )


def generate_article(faker: Faker, **kwargs: Any) -> Article:
    return Article(
        reference=uuid.uuid7(),
        category=kwargs["category"],
        producer=kwargs["producer"],
        product=kwargs["product"] if "product" in kwargs else faker.word(),
        cost_price=kwargs["cost_price"]
        if "cost_price" in kwargs
        else generate_decimal(),
        excise_duty=kwargs["excise_duty"]
        if "excise_duty" in kwargs
        else generate_decimal(),
        social_security_contribution=kwargs["social_security_contribution"]
        if "social_security_contribution" in kwargs
        else generate_decimal(),
        vat_rate=kwargs["vat_rate"]
        if "vat_rate" in kwargs
        else generate_decimal(decimal_places=2),
        distributor=kwargs["distributor"],
        barcode=kwargs["barcode"] if "barcode" in kwargs else faker.ean13(),
        origin=kwargs["origin"],
        color=kwargs["color"]
        if "color" in kwargs
        else random.choice(list(ArticleColor)),
        taste=kwargs["taste"]
        if "taste" in kwargs
        else random.choice(list(ArticleTaste)),
        volume=kwargs["volume"],
        alcohol_by_volume=kwargs["alcohol_by_volume"]
        if "alcohol_by_volume" in kwargs
        else random.uniform(0, 60),
        deposit=kwargs["deposit"],
        created_at=kwargs["created_at"]
        if "created_at" in kwargs
        else faker.date_this_year(),
        updated_at=kwargs["updated_at"]
        if "updated_at" in kwargs
        else faker.date_this_year(),
        store_data=kwargs["store_data"],
    )


# class ArticleEntityFactory(ModelFactory[Article]):
#     @classmethod
#     def build(cls, factory_use_construct: bool = False, **kwargs: Any) -> Article:
#         if "store_data" not in kwargs:
#             kwargs["store_data"] = {
#                 cls.__faker__.slug(): ArticleStoreDataEntityFactory.build()
#                 for _ in range(cls.__random__.choice([1, 2, 3]))
#             }
#         kwargs["deposit"] = ArticleDepositEntityFactory.build()
#         return super().build(**kwargs)


class ArticleFactory(BaseMongoFactory[Article]):
    repository_class = ArticleRepository

    @property
    def category_factory(self) -> CategoryFactory:
        return CategoryFactory(faker=self.faker, database=self.database)

    @property
    def producer_factory(self) -> ProducerFactory:
        return ProducerFactory(faker=self.faker, database=self.database)

    @property
    def distributor_factory(self) -> DistributorFactory:
        return DistributorFactory(faker=self.faker, database=self.database)

    @property
    def origin_factory(self) -> OriginFactory:
        return OriginFactory(faker=self.faker, database=self.database)

    @property
    def volume_factory(self) -> VolumeFactory:
        return VolumeFactory(faker=self.faker, database=self.database)

    @property
    def deposit_factory(self) -> DepositFactory:
        return DepositFactory(faker=self.faker, database=self.database)

    def build(self, *, stores: list[Store] | None = None, **kwargs: Any) -> Article:
        if "category" not in kwargs:
            kwargs["category"] = self.category_factory.create_one().name

        if "producer" not in kwargs:
            kwargs["producer"] = self.producer_factory.create_one().name

        if "distributor" not in kwargs:
            kwargs["distributor"] = self.distributor_factory.create_one().name

        if "origin" not in kwargs:
            kwargs["origin"] = self.origin_factory.create_one().name

        if "volume" not in kwargs:
            volume = self.volume_factory.create_one()
            kwargs["volume"] = ArticleVolume(value=volume.value, unit=volume.unit)

        if "deposit" not in kwargs:
            kwargs["deposit"] = ArticleDeposit(
                unit=self.deposit_factory.create_one().value,
                case=(
                    self.deposit_factory.create_one().value
                    if self.faker.boolean(chance_of_getting_true=50)
                    else None
                ),
                packaging=(
                    random.randint(1, 24)
                    if self.faker.boolean(chance_of_getting_true=50)
                    else None
                ),
            )

        if stores:
            kwargs["store_data"] = {
                store.slug: generate_article_store_data() for store in stores
            }
        else:
            kwargs["store_data"] = {"store_test": generate_article_store_data()}

        return generate_article(self.faker, **kwargs)
