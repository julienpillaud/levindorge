from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

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
