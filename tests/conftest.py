import pytest

from project.app.main import app, db_tables, create_application
from starlette.testclient import TestClient


from project.app.database.db import Db

db_test_engine = Db(testing=True)


@pytest.fixture(scope="module")
def test_app() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db() -> TestClient:

    # Initializing database for testing

    db_test_engine.set_tables(db_tables)

    app = create_application()

    # bind fast api application
    db_test_engine.bind_fastAPI(app)

    # override dependencies for test_db
    db_test_engine.app.dependency_overrides["get_db"] = db_test_engine.get_db

    # binding db_test_engine with starlette TestClient
    db_test_engine.bind_test_client()

    test_client = TestClient(db_test_engine.app)

    db_test_engine.bind_test_client(test_client)

    with TestClient(db_test_engine.app) as test_client:

        try:

            yield db_test_engine

        finally:

            # teardown
            db_test_engine.engine.dispose()

            # Connect to posgres server to drop the database
            teardown_engine = db_test_engine.init_engine()
            conn = teardown_engine.connect()
            conn.execute("DROP TABLE articles")
            conn.execute("DROP TABLE authors")
