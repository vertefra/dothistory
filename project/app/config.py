import os
import logging

from pydantic import BaseSettings
from functools import lru_cache

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", 'development')
    testing: bool = os.getenv("TESTING", False)
    database_url: str = os.getenv("DATABASE_URL")
    database_url_test: str = os.getenv("DATABASE_URL_TEST")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading env settings")
    return Settings()
