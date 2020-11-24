from fastapi import FastAPI
# from sqlalchemy.orm import Session

from project.app.routers import ping_router, authors_router
from project.app.models import authors, articles
from project.app.database.db import db_engine

db_tables = [
    authors.Author,
    articles.Article
]


def create_application():

    application = FastAPI()

    db_engine.bind_fastAPI(application)
    db_engine.set_tables(db_tables)
    db_engine.create_tables()

    application.include_router(ping_router.router)
    application.include_router(
        router=authors_router.router,
        prefix="/authors"
    )
    return application


app = create_application()
