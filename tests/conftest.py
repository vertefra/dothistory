import pytest

from project.app.main import app
from project.app.main import create_application, db_tables
from starlette.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from project.app.config import get_settings
from project.app.database.db import init_db


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db() -> TestClient:

    # Initializing database for testing

    settings = get_settings()
    test_engine = init_db(testing=True)
    TestSession = sessionmaker(
        bind=test_engine, autocommit=False, autoflush=False)

    def get_test_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    # Creating test application

    app = create_application(
        db_engine=test_engine,
        db_tables=db_tables
    )

    # Overriding database dependencies for routes with
    # testing databse

    app.dependency_overrides["get_db"] = get_test_db

    with TestClient(app) as test_client:

        try:

            yield test_client

        finally:

            # teardown
            test_engine.dispose()

            # Connect to posgres server to drop the database
            teardown_engine = create_engine(
                settings.database_url + settings.test_db)
            conn = teardown_engine.connect()
            conn.execute("DROP TABLE articles")
            conn.execute("DROP TABLE authors")
