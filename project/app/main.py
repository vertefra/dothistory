
from fastapi import FastAPI


from project.app.routers import test_router
from project.app.routers import authors_router

from project.app.config import get_settings
from project.app.models import authors, articles
from project.app.database.db import create_tables

db_tables = [
    authors.Author,
    articles.Article
]


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

create_tables(db_tables)
