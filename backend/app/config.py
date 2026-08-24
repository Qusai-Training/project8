import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads DATABASE_URL from .env with fallback to default PostgreSQL URI
    DATABASE_URL: str = "postgresql://postgres:123456@localhost:5432/project8"
    
    # Operational thresholds & file paths
    FAILED_LOGIN_THRESHOLD: int = 5
    BLACKLIST_FILE_PATH: str = "blacklist.txt"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()