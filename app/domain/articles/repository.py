from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.entities import EntityId, PaginatedResponse
from app.domain.protocols.repository import RepositoryProtocol


class ArticleRepositoryProtocol(RepositoryProtocol[Article], Protocol):
    def get_by_ids(
        self,
        article_ids: list[EntityId],
        /,
    ) -> PaginatedResponse[Article]: ...

    def exists_by_producer(self, producer: str) -> bool: ...
