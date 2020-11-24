from fastapi import FastAPI
# from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from project.app.routers import ping_router, authors_router
from project.app.models import authors, articles
from project.app.database.db import create_tables, engine

db_tables = [
    authors.Author,
    articles.Article
]


def create_application(
        db_engine: Engine = engine,
        db_tables: list = db_tables) -> FastAPI:
    ''' For testing: create a database engine for testing
    with init_db(testing=True) and feed it to create_application
    in order to have a db_test active '''

    application = FastAPI()
    create_tables(db_tables, engine)

    application.include_router(ping_router.router)
    application.include_router(
        router=authors_router.router,
        prefix="/authors"
    )
    return application


app = create_application()
