from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App
    APP_NAME: str = "akiralab-agent"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Firebase
    FIREBASE_DATABASE_URL: str
    FIREBASE_SERVICE_ACCOUNT_KEY_PATH: str = "firebase-service-account.json"

    # API
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
