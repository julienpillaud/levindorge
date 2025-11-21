from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.entities import PaginatedResponse
from app.infrastructure.repository.mongo_repository import MongoRepository


class ArticleRepository(MongoRepository[Article], ArticleRepositoryProtocol):
    domain_entity_type = Article
    collection_name = "articles"
    searchable_fields = (
        "producer",
        "product",
        "color",
        "taste",
        "region",
        "distributor",
        "category",
    )

    def get_by_display_group(
        self,
        display_group: str,
    ) -> PaginatedResponse[Article]:
        article_types = self.database["types"].find({"list_category": display_group})
        article_types_names = [x["name"] for x in article_types]
        return self.get_all(
            filters={"type": {"$in": article_types_names}},
            sort={"type": 1, "region": 1, "name.name1": 1, "name.name2": 1},
            page=1,
            limit=1000,
        )
