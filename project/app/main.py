from fastapi import FastAPI

from project.app.routers import test_router
from project.app.config import get_settings
from project.app.database.db import create_db_if_not_exists, init_db


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(test_router.router)
    return application


settings = get_settings()

app = create_application()
db_engine = init_db(settings.database_url)
create_db_if_not_exists(db_engine, 'dev_db')
create_db_if_not_exists(db_engine, 'test_db')
