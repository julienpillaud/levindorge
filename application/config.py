from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENVIRONMENT: str
    SECRET_KEY: str
    MONGODB_URI: str
    MONGODB_DATABASE: str
    ROLLBAR_ACCESS_TOKEN: str


settings = Settings()
