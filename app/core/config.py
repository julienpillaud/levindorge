from zoneinfo import ZoneInfo

from pydantic import RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.paths import AppPaths


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
    )

    project_name: str = "Le Vin d'Orge"
    api_version: str = "0.0.1"
    environment: str
    secret_key: str
    app_path: AppPaths = AppPaths()
    zone_info: ZoneInfo = ZoneInfo("Europe/Paris")
    logfire_token: str = ""

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int = 27017
    mongo_database: str

    redis_host: str
    redis_port: int = 6379
    redis_scheme: str = "redis"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def mongo_uri(self) -> str:
        if self.mongo_host == "localhost":
            return (
                f"mongodb://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}:{self.mongo_port}"
            )
        else:
            return (
                f"mongodb+srv://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}/?retryWrites=true&w=majority"
            )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn.build(
            host=self.redis_host,
            port=self.redis_port,
            scheme=self.redis_scheme,
        )
