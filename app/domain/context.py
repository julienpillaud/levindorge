from typing import Protocol

from cleanstack.domain import UnitOfWorkProtocol

from app.domain._shared.protocols.event_publisher import EventPublisherProtocol
from app.domain._shared.protocols.pos_manager import POSManagerProtocol
from app.domain._shared.protocols.repository import RepositoryProtocol
from app.domain.articles.repository import ArticleRepositoryProtocol
from app.domain.categories.repository import CategoryRepositoryProtocol
from app.domain.producers.repository import ProducerRepositoryProtocol
from app.domain.stores.repository import StoreRepositoryProtocol
from app.domain.users.repository import UserRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def repository(self) -> RepositoryProtocol: ...

    @property
    def store_repository(self) -> StoreRepositoryProtocol: ...

    @property
    def user_repository(self) -> UserRepositoryProtocol: ...

    @property
    def category_repository(self) -> CategoryRepositoryProtocol: ...

    @property
    def article_repository(self) -> ArticleRepositoryProtocol: ...

    @property
    def producer_repository(self) -> ProducerRepositoryProtocol: ...

    @property
    def pos_manager(self) -> POSManagerProtocol: ...

    @property
    def event_publisher(self) -> EventPublisherProtocol: ...
