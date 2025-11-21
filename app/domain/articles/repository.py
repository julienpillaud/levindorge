from typing import Protocol

from app.domain._shared.protocols.base_repository import RepositoryProtocol
from app.domain.articles.entities import Article
from app.domain.entities import PaginatedResponse


class ArticleRepositoryProtocol(RepositoryProtocol[Article], Protocol):
    def get_by_display_group(
        self,
        display_group: str,
    ) -> PaginatedResponse[Article]: ...
