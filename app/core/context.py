from cleanstack.domain import UnitOfWorkProtocol
from cleanstack.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from pymongo.client_session import ClientSession

from app.core.config.settings import Settings
from app.domain.context import ContextProtocol
from app.infrastructure.cache_manager.redis_cache_manager import RedisCacheManager
from app.infrastructure.event_publisher.faststream_event_publisher import (
    FastStreamEventPublisher,
)
from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.deposits import DepositRepository
from app.infrastructure.repository.distributors import DistributorRepository
from app.infrastructure.repository.inventories import InventoryRepository
from app.infrastructure.repository.origins import OriginRepository
from app.infrastructure.repository.price_labels import PriceLabelRepository
from app.infrastructure.repository.producers import ProducerRepository
from app.infrastructure.repository.stores import StoreRepository
from app.infrastructure.repository.volumes import VolumeRepository
from app.infrastructure.supabase.identity_provider import SupabaseIdentityProvider
from app.infrastructure.tactill.manager import TactillManager


class Context(ContextProtocol):
    def __init__(
        self,
        settings: Settings,
        mongo_context: MongoContext,
        mongo_uow: MongoUnitOfWork | None = None,
    ):
        self.settings = settings
        self.mongo_context = mongo_context
        self.mongo_uow = mongo_uow
        self.members = self._get_members()

    def _get_members(self) -> list[UnitOfWorkProtocol]:
        members: list[UnitOfWorkProtocol] = []
        if self.mongo_uow:
            members.append(self.mongo_uow)
        return members

    @property
    def _mongo_session(self) -> ClientSession | None:
        return self.mongo_uow.session if self.mongo_uow else None

    @property
    def identity_provider(self) -> SupabaseIdentityProvider:
        return SupabaseIdentityProvider(settings=self.settings)

    @property
    def store_repository(self) -> StoreRepository:
        return StoreRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def category_repository(self) -> CategoryRepository:
        return CategoryRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def article_repository(self) -> ArticleRepository:
        return ArticleRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def producer_repository(self) -> ProducerRepository:
        return ProducerRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def distributor_repository(self) -> DistributorRepository:
        return DistributorRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def origin_repository(self) -> OriginRepository:
        return OriginRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def volume_repository(self) -> VolumeRepository:
        return VolumeRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def deposit_repository(self) -> DepositRepository:
        return DepositRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def price_label_repository(self) -> PriceLabelRepository:
        return PriceLabelRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def inventory_repository(self) -> InventoryRepository:
        return InventoryRepository(
            database=self.mongo_context.database,
            session=self._mongo_session,
        )

    @property
    def pos_manager(self) -> TactillManager:
        return TactillManager()

    @property
    def cache_manager(self) -> RedisCacheManager:
        return RedisCacheManager(settings=self.settings)

    @property
    def event_publisher(self) -> FastStreamEventPublisher:
        return FastStreamEventPublisher(settings=self.settings)
