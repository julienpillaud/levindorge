from typing import Protocol

from cleanstack.domain import RepositoryProtocol
from cleanstack.entities import EntityId, PaginatedResponse

from app.domain.articles.entities import Article


class ArticleRepositoryProtocol(RepositoryProtocol[Article], Protocol):
    def create_many(self, articles: list[Article]) -> list[Article]: ...

    def get_by_ids(
        self,
        article_ids: list[EntityId],
        /,
    ) -> PaginatedResponse[Article]: ...
