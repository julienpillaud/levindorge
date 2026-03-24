from cleanstack.entities import (
    EntityId,
    FilterEntity,
    FilterOperator,
    PaginatedResponse,
    SortEntity,
    SortOrder,
)
from cleanstack.infrastructure.mongo.base import MongoRepository, MongoRepositoryError

from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol


class ArticleRepository(MongoRepository[Article], ArticleRepositoryProtocol):
    domain_entity_type = Article
    collection_name = "articles"
    searchable_fields = (
        "reference",
        "category",
        "producer",
        "product",
        "distributor",
        "origin",
        "color",
        "taste",
    )

    def create_many(self, articles: list[Article]) -> list[Article]:
        entities = [self._to_database_entity(entity) for entity in articles]

        result = self.collection.insert_many(entities)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to insert entities")

        return articles

    def get_by_ids(self, article_ids: list[EntityId], /) -> PaginatedResponse[Article]:
        return self.get_all(
            filters=[
                FilterEntity(
                    field="id",
                    value=[str(article_id) for article_id in article_ids],
                    operator=FilterOperator.IN,
                )
            ],
            sort=[
                SortEntity(field="category", order=SortOrder.ASC),
                SortEntity(field="producer", order=SortOrder.ASC),
                SortEntity(field="product", order=SortOrder.ASC),
            ],
        )

    def get_by_id(self, entity_id: EntityId, /) -> Article | None:
        result = self.collection.find_one({"_id": entity_id}, session=self.session)
        return self._to_domain_entity(result) if result else None
