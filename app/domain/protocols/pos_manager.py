from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.commons.entities import DisplayGroup
from app.domain.pos.entities import POSArticle
from app.domain.stores.entities import Store


class POSManagerProtocol(Protocol):
    def get_articles(self, _: Store, /) -> list[POSArticle]: ...

    def create_article(
        self,
        store: Store,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> POSArticle: ...

    def update_article(
        self,
        store: Store,
        /,
        article: Article,
        category_name: str,
        display_group: DisplayGroup,
    ) -> None: ...

    def delete_article_by_reference(
        self,
        store: Store,
        /,
        reference: str,
    ) -> None: ...

    def reset_stocks_by_category(
        self,
        store: Store,
        /,
        category: str,
    ) -> None: ...
