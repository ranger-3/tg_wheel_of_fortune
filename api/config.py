"""Application settings loaded from .env and validated via Pydantic."""

import sys

from pydantic import Field, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from logging_config import logger

__all__ = ["settings"]


class Settings(BaseSettings):
    bot_token: SecretStr
    channel_username: str = Field(..., min_length=1)
    store_api_key: SecretStr
    store_api_url: str = Field(..., min_length=1)

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("BOT_TOKEN must be set and not empty")
        return value

    @field_validator("store_api_key")
    @classmethod
    def validate_store_api_key(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("STORE_API_KEY must be set and not empty")
        return value


try:
    settings = Settings()
except ValidationError:
    logger.exception(
        "Failed to load environment variables from .env or failed validation:"
    )
    sys.exit(1)
