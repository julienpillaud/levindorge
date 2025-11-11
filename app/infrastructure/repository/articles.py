from app.domain.articles.entities import Article
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.commons.entities import DisplayGroup
from app.domain.entities import PaginatedResponse, Pagination
from app.infrastructure.repository.mongo_repository import MongoRepository


class ArticleRepository(MongoRepository[Article], ArticleRepositoryProtocol):
    domain_model = Article
    collection_name = "articles"
    searchable_fields = (
        "name.name1",
        "name.name2",
        "color",
        "taste",
        "region",
        "distributor",
        "type",
    )

    def get_by_display_group(
        self,
        display_group: DisplayGroup,
    ) -> PaginatedResponse[Article]:
        article_types = self.database["types"].find({"list_category": display_group})
        article_types_names = [x["name"] for x in article_types]
        return self.get_all(
            filters={"type": {"$in": article_types_names}},
            sort={"type": 1, "region": 1, "name.name1": 1, "name.name2": 1},
            pagination=Pagination(page=1, limit=1000),
        )
