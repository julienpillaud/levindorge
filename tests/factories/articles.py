from typing import Any

from polyfactory.factories.pydantic_factory import ModelFactory

from app.domain.articles.entities import Article, ArticleStoreData
from app.domain.stores.entities import Store
from app.infrastructure.repository.articles import ArticleRepository
from tests.factories.base import BaseMongoFactory
from tests.factories.categories import CategoryFactory


class ArticleStoreDataEntityFactory(ModelFactory[ArticleStoreData]): ...


class ArticleEntityFactory(ModelFactory[Article]):
    @classmethod
    def build(cls, **kwargs: Any) -> Article:
        if "store_data" not in kwargs:
            kwargs["store_data"] = {
                cls.__faker__.slug(): ArticleStoreDataEntityFactory.build()
                for _ in range(cls.__random__.choice([1, 2, 3]))
            }
        return super().build(**kwargs)


class ArticleFactory(BaseMongoFactory[Article]):
    repository_class = ArticleRepository

    @property
    def category_factory(self) -> CategoryFactory:
        return CategoryFactory(database=self.database)

    def build(self, *, stores: list[Store] | None = None, **kwargs: Any) -> Article:
        if "category" not in kwargs:
            kwargs["category"] = self.category_factory.create_one().name

        if stores:
            kwargs["store_data"] = {
                store.slug: ArticleStoreDataEntityFactory.build() for store in stores
            }

        return ArticleEntityFactory.build(**kwargs)
