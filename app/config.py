from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENVIRONMENT: str
    SECRET_KEY: str
    MONGODB_URI: str
    MONGODB_DATABASE: str
    WIZISHOP_EMAIL: str
    WIZISHOP_PASSWORD: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    LOGFIRE_TOKEN: str
    LOGFIRE_SERVICE_NAME: str


settings = Settings()  # type: ignore
