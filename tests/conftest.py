import pytest

from project.app import main
from project.app.main import create_application, db_tables
from starlette.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from project.app.config import get_settings
from project.app.database.db import init_db, create_tables, get_db


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db() -> TestClient:

    settings = get_settings()

    with TestClient(create_application()) as test_client:
        print(" - Initializing test database")

        test_engine = init_db(testing=True)

        TestSession = sessionmaker(
            bind=test_engine, autocommit=False, autoflush=False)

        db = get_db(TestSession)

        # setting a db attrribute to app in order to bind the
        # newly created database instance to test_app

        test_client.__setattr__("db", db)

        create_tables(db_tables, test_engine)
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
