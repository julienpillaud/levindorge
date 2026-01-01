from bson import ObjectId

from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.entities import EntityId, PaginatedResponse
from app.infrastructure.repository.base import MongoRepository


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

    def get_by_ids(self, article_ids: list[EntityId], /) -> PaginatedResponse[Article]:
        return self.get_all(
            filters={"_id": {"$in": [ObjectId(id_) for id_ in article_ids]}},
            sort={"type": 1, "region": 1, "name.name1": 1, "name.name2": 1},
        )

    def exists_by_producer(self, producer: str) -> bool:
        return self.collection.find_one({"producer": producer}) is not None

    def exists_by_distributor(self, distributor: str) -> bool:
        return self.collection.find_one({"distributor": distributor}) is not None
