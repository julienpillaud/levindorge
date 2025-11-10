from bson import ObjectId
from cleanstack.exceptions import NotFoundError
from pymongo import ASCENDING

from app.domain.articles.entities import Article
from app.domain.entities import EntityId
from app.domain.protocols.repository import ArticleRepositoryProtocol
from app.infrastructure.repository.exceptions import MongoRepositoryError
from app.infrastructure.repository.protocol import MongoRepositoryProtocol


class ArticleRepository(MongoRepositoryProtocol, ArticleRepositoryProtocol):
    def get_articles(self) -> list[Article]:
        articles = self.database["articles"].find().sort("type")
        return [Article.model_validate(article) for article in articles]

    def get_articles_by_display_group(self, display_group: str) -> list[Article]:
        categories = self.database["types"].find({"list_category": display_group})
        category_names = [x["name"] for x in categories]

        articles = (
            self.database["articles"]
            .find({"type": {"$in": category_names}})
            .sort(
                [
                    ("type", ASCENDING),
                    ("region", ASCENDING),
                    ("name.name1", ASCENDING),
                    ("name.name2", ASCENDING),
                ]
            )
        )
        return [Article(**article) for article in articles]

    def get_article(self, article_id: EntityId) -> Article | None:
        article = self.database["articles"].find_one({"_id": ObjectId(article_id)})
        return Article(**article) if article else None

    def create_article(self, article: Article) -> Article:
        result = self.database["articles"].insert_one(
            article.model_dump(exclude={"id"})
        )
        return self._get_article_by_id(article_id=result.inserted_id)

    def update_article(self, article: Article) -> Article:
        result = self.database["articles"].replace_one(
            {"_id": ObjectId(article.id)},
            article.model_dump(exclude={"id"}),
        )
        if not result.modified_count:
            raise MongoRepositoryError()

        return self._get_article_by_id(article_id=article.id)

    def delete_article(self, article: Article) -> None:
        self.database["articles"].delete_one({"_id": ObjectId(article.id)})

    def _get_article_by_id(self, article_id: str) -> Article:
        article_db = self.database["articles"].find_one({"_id": ObjectId(article_id)})
        if not article_db:
            raise NotFoundError()

        return Article(**article_db)
