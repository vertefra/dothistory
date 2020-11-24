
import asyncio

from fastapi import FastAPI

from project.app.routers import ping_router, authors_router
from project.app.config import get_settings
from project.app.models import authors, articles
from project.app.database.db import create_tables, engine

db_tables = [
    authors.Author,
    articles.Article
]


def create_application() -> FastAPI:
    application = FastAPI()

    # creating tables in async
    asyncio.create_task(create_tables(db_tables, engine))
    print(" - go on setting up routes")

    application.include_router(ping_router.router)

    application.include_router(
        router=authors_router.router,
        prefix="/authors"
    )
    return application


settings = get_settings()
app = create_application()
# create_tables(db_tables, engine)
