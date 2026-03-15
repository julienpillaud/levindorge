from enum import StrEnum
from zoneinfo import ZoneInfo

from pydantic import AmqpDsn, MongoDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.paths import AppPaths


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    project_name: str = "Le Vin d'Orge"
    app_version: str
    environment: AppEnvironment
    secret_key: str
    access_token_expire: int = 3600  # 1 hour
    refresh_token_expire: int = 7 * 24 * 60 * 60  # 7 days
    app_path: AppPaths = AppPaths()
    zone_info: ZoneInfo = ZoneInfo("Europe/Paris")
    logfire_token: str = ""

    supabase_url: str
    supabase_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "authenticated"

    mongo_user: str | None = None
    mongo_password: str | None = None
    mongo_host: str
    mongo_port: int = 27017
    mongo_rs_name: str = "rs0"
    mongo_database: str

    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_vhost: str = "/"

    redis_host: str
    redis_port: int = 6379

    @computed_field
    @property
    def mongo_uri(self) -> str:
        if self.mongo_host in {"localhost", "127.0.0.1"}:
            query = f"replicaSet={self.mongo_rs_name}" if self.mongo_rs_name else None
            mongo_dsn = MongoDsn.build(
                scheme="mongodb",
                host="localhost",
                username=self.mongo_user,
                password=self.mongo_password,
                port=self.mongo_port,
                query=query,
            )
            return str(mongo_dsn)
        else:
            return (
                f"mongodb+srv://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}/?retryWrites=true&w=majority"
            )

    @computed_field
    @property
    def rabbitmq_dsn(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.rabbitmq_user,
            password=self.rabbitmq_password,
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            path=self.rabbitmq_vhost,
        )

    @computed_field
    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            path="0",
        )
