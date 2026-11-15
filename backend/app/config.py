from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings. Values come from environment variables (see .env.example)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "DocVerify AI"
    database_url: str = "sqlite:///./docverify.db"
    secret_key: str = "change-me-in-production"
    access_token_minutes: int = 60

    upload_dir: str = "./uploads"
    max_upload_mb: int = 10

    qdrant_url: str = "http://localhost:6333"
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    # first admin account, created on startup if it does not exist yet
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin12345"
    # optional demo reviewer (leave empty to skip)
    reviewer_email: str = ""
    reviewer_password: str = ""

    # login protection
    max_failed_logins: int = 5
    lock_minutes: int = 15


@lru_cache
def get_settings() -> Settings:
    return Settings()
