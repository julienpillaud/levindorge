from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.entities import PaginatedResponse
from app.domain.protocols.base_repository import RepositoryProtocol


class ArticleRepositoryProtocol(RepositoryProtocol[Article], Protocol):
    def get_by_display_group(
        self,
        display_group: DisplayGroup,
    ) -> PaginatedResponse[Article]: ...
