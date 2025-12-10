from collections.abc import Iterator
from contextlib import contextmanager
from functools import cached_property

from fastapi import FastAPI
from faststream.redis import RedisBroker
from pymongo import MongoClient
from supabase import Client
from supabase.lib.client_options import SyncClientOptions

from app.core.config.settings import Settings
from app.domain.context import ContextProtocol
from app.domain.domain import Domain
from app.infrastructure.event_publisher import FastStreamEventPublisher
from app.infrastructure.repository.articles import ArticleRepository
from app.infrastructure.repository.base import MongoRepository
from app.infrastructure.repository.categories import CategoryRepository
from app.infrastructure.repository.deposits import DepositRepository
from app.infrastructure.repository.distributors import DistributorRepository
from app.infrastructure.repository.mongo_repository import MongoDocument
from app.infrastructure.repository.origins import OriginRepository
from app.infrastructure.repository.producers import ProducerRepository
from app.infrastructure.repository.stores import StoreRepository
from app.infrastructure.repository.users import UserRepository
from app.infrastructure.repository.volumes import VolumeRepository
from app.infrastructure.supabase.identity_provider import SupabaseIdentityProvider
from app.infrastructure.tactill.manager import TactillManager


class BaseContext(ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: MongoClient[MongoDocument] = MongoClient(settings.mongo_uri)
        self.database = self.client[settings.mongo_database]
        self.broker = RedisBroker(str(settings.redis_dsn))

    @cached_property
    def supabase_client(self) -> Client:
        return Client(
            supabase_url=self.settings.supabase_url,
            supabase_key=self.settings.supabase_key,
            options=SyncClientOptions(
                auto_refresh_token=False,
                persist_session=False,
            ),
        )

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class Context(BaseContext):
    @property
    def identity_provider(self) -> SupabaseIdentityProvider:
        return SupabaseIdentityProvider(client=self.supabase_client)

    @property
    def repository(self) -> MongoRepository:
        return MongoRepository(database=self.database)

    @property
    def store_repository(self) -> StoreRepository:
        return StoreRepository(database=self.database)

    @property
    def user_repository(self) -> UserRepository:
        return UserRepository(database=self.database)

    @property
    def category_repository(self) -> CategoryRepository:
        return CategoryRepository(database=self.database)

    @property
    def article_repository(self) -> ArticleRepository:
        return ArticleRepository(database=self.database)

    @property
    def producer_repository(self) -> ProducerRepository:
        return ProducerRepository(database=self.database)

    @property
    def distributor_repository(self) -> DistributorRepository:
        return DistributorRepository(database=self.database)

    @property
    def origin_repository(self) -> OriginRepository:
        return OriginRepository(database=self.database)

    @property
    def volume_repository(self) -> VolumeRepository:
        return VolumeRepository(database=self.database)

    @property
    def deposit_repository(self) -> DepositRepository:
        return DepositRepository(database=self.database)

    @property
    def pos_manager(self) -> TactillManager:
        return TactillManager()

    @property
    def event_publisher(self) -> FastStreamEventPublisher:
        return FastStreamEventPublisher(broker=self.broker)


def initialize_app(settings: Settings, app: FastAPI) -> None:
    context = Context(settings=settings)
    domain = Domain(context=context)
    app.state.domain = domain
