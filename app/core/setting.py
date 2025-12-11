"""Configuration definition."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "settings"]

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class EnvSettingsOptions(Enum):
    production = "production"
    staging = "staging"
    development = "dev"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Project Configuration
    ENV_SETTING: EnvSettingsOptions = Field(
        default=EnvSettingsOptions.development,
        description="Environment setting: production, staging, or dev"
    )

    # Database Configuration
    # Example "postgresql+asyncpg://username:password@localhost:5432/db_name"
    PG_DSN: str = Field(
        default="postgresql+asyncpg://username:password@localhost:5432/db_name",
        description="PostgreSQL DSN with asyncpg driver"
    )

    # Connection Pool Configuration
    DB_POOL_SIZE: int = Field(
        default=5,
        description="Number of connections to keep in the pool"
    )
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        description="Max number of connections that can be created beyond pool_size"
    )
    DB_POOL_TIMEOUT: int = Field(
        default=30,
        description="Seconds to wait before giving up on getting a connection from the pool"
    )
    DB_POOL_RECYCLE: int = Field(
        default=3600,
        description="Seconds after which a connection is automatically recycled (prevents stale connections)"
    )
    DB_POOL_PRE_PING: bool = Field(
        default=True,
        description="Enable connection health checks before using from pool"
    )


settings = Settings()
