from functools import cached_property

from app.core.config.settings import Settings
from app.core.uow import UnitOfWork
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
from app.infrastructure.repository.users import UserRepository
from app.infrastructure.repository.volumes import VolumeRepository
from app.infrastructure.supabase.identity_provider import SupabaseIdentityProvider
from app.infrastructure.tactill.manager import TactillManager


class Context(ContextProtocol):
    def __init__(self, settings: Settings, uow: UnitOfWork):
        self.settings = settings
        self.uow = uow

    @cached_property
    def identity_provider(self) -> SupabaseIdentityProvider:
        return SupabaseIdentityProvider(settings=self.settings)

    @cached_property
    def store_repository(self) -> StoreRepository:
        return StoreRepository(database=self.uow.mongo.database)

    @cached_property
    def user_repository(self) -> UserRepository:
        return UserRepository(database=self.uow.mongo.database)

    @cached_property
    def category_repository(self) -> CategoryRepository:
        return CategoryRepository(database=self.uow.mongo.database)

    @cached_property
    def article_repository(self) -> ArticleRepository:
        return ArticleRepository(database=self.uow.mongo.database)

    @cached_property
    def producer_repository(self) -> ProducerRepository:
        return ProducerRepository(database=self.uow.mongo.database)

    @cached_property
    def distributor_repository(self) -> DistributorRepository:
        return DistributorRepository(database=self.uow.mongo.database)

    @cached_property
    def origin_repository(self) -> OriginRepository:
        return OriginRepository(database=self.uow.mongo.database)

    @cached_property
    def volume_repository(self) -> VolumeRepository:
        return VolumeRepository(database=self.uow.mongo.database)

    @cached_property
    def deposit_repository(self) -> DepositRepository:
        return DepositRepository(database=self.uow.mongo.database)

    @cached_property
    def price_label_repository(self) -> PriceLabelRepository:
        return PriceLabelRepository(database=self.uow.mongo.database)

    @cached_property
    def inventory_repository(self) -> InventoryRepository:
        return InventoryRepository(database=self.uow.mongo.database)

    @cached_property
    def pos_manager(self) -> TactillManager:
        return TactillManager()

    @cached_property
    def cache_manager(self) -> RedisCacheManager:
        return RedisCacheManager(settings=self.settings)

    @cached_property
    def event_publisher(self) -> FastStreamEventPublisher:
        return FastStreamEventPublisher(settings=self.settings)
