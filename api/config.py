"""Application settings loaded from .env and validated via Pydantic."""

import sys

from logging_config import logger
from pydantic import Field, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    bot_token: SecretStr
    channel_username: str = Field(..., min_length=1)

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("BOT_TOKEN must be set and not empty")
        return value


try:
    settings = Settings()
except ValidationError:
    logger.exception(
        "Failed to load environment variables from .env or failed validation:"
    )
    sys.exit(1)
