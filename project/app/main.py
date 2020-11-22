from fastapi import FastAPI

from project.app.routers import test_router
from project.app.routers import authors_router

from project.app.config import get_settings
from project.app.database.db import create_tables, engine


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(test_router.router)
    application.include_router(
        router=authors_router.router,
        prefix="/authors"
    )
    return application


settings = get_settings()
app = create_application()


@app.on_event("startup")
def startup():

    if create_tables(engine):
        print("tables created")
