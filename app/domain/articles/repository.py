from typing import Protocol

from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.articles.entities import Article
from app.domain.entities import PaginatedResponse
from app.domain.types import EntityId


class ArticleRepositoryProtocol(RepositoryProtocol[Article], Protocol):
    def get_by_ids(
        self,
        article_ids: list[EntityId],
        /,
    ) -> PaginatedResponse[Article]: ...
