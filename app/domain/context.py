from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.domain.protocols.event_publisher import EventPublisherProtocol
from app.domain.protocols.pos_manager import POSManagerProtocol
from app.domain.protocols.repository import RepositoryProtocol
from app.domain.stores.repository import StoreRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...

    @property
    def store_repository(self) -> StoreRepositoryProtocol: ...

    @property
    def category_repository(self) -> CategoryRepositoryProtocol: ...

    @property
    def article_repository(self) -> ArticleRepositoryProtocol: ...

    @property
    def pos_manager(self) -> POSManagerProtocol: ...

    @property
    def event_publisher(self) -> EventPublisherProtocol: ...
