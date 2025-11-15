from cleanstack.exceptions import NotFoundError

from app.domain.category_groups.entities import CategoryGroup
from app.domain.commons.entities import ArticleType, DisplayGroup
from app.domain.protocols.repository import ArticleTypeRepositoryProtocol
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class ArticleTypeRepository(MongoRepositoryProtocol, ArticleTypeRepositoryProtocol):
    def get_article_types(
        self,
        name: str | None = None,
        display_group: DisplayGroup | None = None,
    ) -> list[ArticleType]:
        query_filter = {}
        if name is not None:
            query_filter["name"] = name
        if display_group is not None:
            query_filter["list_category"] = display_group

        article_types = self.database["types"].find(query_filter)
        return [ArticleType(**article_type) for article_type in article_types]

    def get_article_type_by_name(self, name: str) -> ArticleType:
        article_type = self.database["types"].find_one({"name": name})
        if not article_type:
            raise NotFoundError()

        return ArticleType(**article_type)

    def get_article_types_by_list(
        self,
        display_group: DisplayGroup,
    ) -> list[ArticleType]:
        article_types = self.database["types"].find({"list_category": display_group})
        return [ArticleType(**article_type) for article_type in article_types]

    def get_category_group(self, slug: str) -> CategoryGroup:
        category_group = self.database["category_groups"].find_one({"slug": slug})
        if not category_group:
            raise NotFoundError()

        return CategoryGroup(**category_group)

    def get_category_group_by_category(
        self,
        category_name: str,
    ) -> CategoryGroup:
        category = self.database["types"].find_one({"name": category_name})
        if not category:
            raise NotFoundError()

        category_group = self.database["category_groups"].find_one(
            {"slug": category["list_category"]}
        )
        if not category_group:
            raise NotFoundError()

        return CategoryGroup(**category_group)
