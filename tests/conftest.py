import pytest
from project.app import main
# from project.app.main import create_application
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    with TestClient(main.app) as test_client:
        yield test_client
