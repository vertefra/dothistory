import pytest

from project.app import main
from project.app.main import create_application
from starlette.testclient import TestClient

from project.app.config import get_settings
from project.app.database.db import init_db, create_tables, get_db


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db() -> TestClient:
    with TestClient(create_application()) as test_client:
        print(" - Initializing test database")
        settings = get_settings()
        engine = init_db(settings.database_url_test, "test_db")
        db = get_db(engine)
        test_client.__setattr__("db", db)
        if create_tables(engine):
            print('- Test tables Created')
        yield test_client
