from fastapi import FastAPI

from project.app.routers import test_router
from project.app.config import get_settings
from project.app.database.db import init_db, create_tables


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(test_router.router)
    return application


settings = get_settings()
app = create_application()


@app.on_event("startup")
def startup():
    engine = init_db(settings.database_url)
    if create_tables(engine):
        print("tables created")
