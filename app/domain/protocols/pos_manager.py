from typing import Protocol

from app.domain.articles.entities import Article
from app.domain.categories.entities import Category
from app.domain.pos.entities import POSArticle
from app.domain.stores.entities import Store


class POSManagerProtocol(Protocol):
    def get_articles(self, _: Store, /) -> list[POSArticle]: ...

    def create_article(
        self,
        store: Store,
        /,
        article: Article,
        category: Category,
    ) -> POSArticle: ...

    def update_article(
        self,
        store: Store,
        /,
        article: Article,
        category: Category,
    ) -> None: ...

    def delete_article(
        self,
        store: Store,
        /,
        article: Article,
    ) -> None: ...

    def reset_stocks_by_category(
        self,
        store: Store,
        /,
        category: str,
    ) -> None: ...
