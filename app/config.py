import secrets

from pydantic import MongoDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENVIRONMENT: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    WIZISHOP_EMAIL: str
    WIZISHOP_PASSWORD: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    LOGFIRE_TOKEN: str
    LOGFIRE_SERVICE_NAME: str

    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_DATABASE: str

    @computed_field  # type: ignore[misc]
    @property
    def MONGODB_URI(self) -> MongoDsn:
        return MultiHostUrl.build(
            scheme="mongodb+srv",
            username=self.MONGODB_USER,
            password=self.MONGODB_PASSWORD,
            host=self.MONGODB_HOST,
            query="retryWrites=true&w=majority",
        )


settings = Settings()  # type: ignore
