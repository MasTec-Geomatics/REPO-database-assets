"""Settings read from the environment, plus a local .env file in development."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised with a required setting is missing."""


@dataclass(frozen=True, slots=True)
class Settings:
    database_url: str = field(repr=False)  # holds the password; keep out of logs


def load_settings() -> Settings:
    load_dotenv()
    database_url = os.environ.get("REPO_DATABASE_URL")
    if not database_url:
        raise ConfigError("REPO_DATABASE_URL is not set")
    return Settings(database_url=database_url)
