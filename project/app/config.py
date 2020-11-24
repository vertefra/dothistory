import os
import logging

from pydantic import BaseSettings
from functools import lru_cache

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", 'development')
    testing: bool = os.getenv("TESTING", False)
    database_url: str = os.getenv("DATABASE_URL")
    test_db: str = os.getenv("TEST_DB")
    dev_db: str = os.getenv("DEV_DB")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading env settings")
    return Settings()
