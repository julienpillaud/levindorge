from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.shops.entities import Shop


class POSManagerProtocol(Protocol):
    def create_article(
        self,
        shop: Shop,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> None: ...
    def update_article(
        self,
        shop: Shop,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> None: ...
    def delete_article_by_reference(
        self,
        shop: Shop,
        /,
        reference: str,
    ) -> None: ...
