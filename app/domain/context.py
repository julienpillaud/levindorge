from typing import TYPE_CHECKING, Protocol

from cleanstack.domain import UnitOfWorkProtocol

if TYPE_CHECKING:
    from app.domain.articles.repository import ArticleRepositoryProtocol
    from app.domain.categories.repository import CategoryRepositoryProtocol
    from app.domain.deposits.repository import DepositRepositoryProtocol
    from app.domain.distributors.repository import DistributorRepositoryProtocol
    from app.domain.inventories.repository import InventoryRepositoryProtocol
    from app.domain.origins.repository import OriginRepositoryProtocol
    from app.domain.price_labels.repository import PriceLabelRepositoryProtocol
    from app.domain.producers.repository import ProducerRepositoryProtocol
    from app.domain.protocols.cache_manager import CacheManagerProtocol
    from app.domain.protocols.event_publisher import EventPublisherProtocol
    from app.domain.protocols.identity_provider import IdentityProviderProtocol
    from app.domain.protocols.pos_manager import POSManagerProtocol
    from app.domain.stores.repository import StoreRepositoryProtocol
    from app.domain.users.repository import UserRepositoryProtocol
    from app.domain.volumes.repository import VolumeRepositoryProtocol


class ContextProtocol(UnitOfWorkProtocol, Protocol):
    @property
    def identity_provider(self) -> IdentityProviderProtocol: ...

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
    def distributor_repository(self) -> DistributorRepositoryProtocol: ...

    @property
    def origin_repository(self) -> OriginRepositoryProtocol: ...

    @property
    def volume_repository(self) -> VolumeRepositoryProtocol: ...

    @property
    def deposit_repository(self) -> DepositRepositoryProtocol: ...

    @property
    def price_label_repository(self) -> PriceLabelRepositoryProtocol: ...

    @property
    def inventory_repository(self) -> InventoryRepositoryProtocol: ...

    @property
    def pos_manager(self) -> POSManagerProtocol: ...

    @property
    def cache_manager(self) -> CacheManagerProtocol: ...

    @property
    def event_publisher(self) -> EventPublisherProtocol: ...
