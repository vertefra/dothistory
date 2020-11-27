import json
from project.app.schemas import authors


def test_create_author(test_app_with_db):

    payload = authors.AuthorRequestPayload(
        name="Test Name",
        email="vertel@gmail.com",
        password="Test Password"
    )

    test_client = test_app_with_db.TestClient

    response = test_client.post(
        '/authors/', data=json.dumps(payload.dict()))

    response_json = response.json()

    assert response.status_code == 201
    assert response_json["id"] == 1
    assert response_json["name"] == "Test Name"
    assert response_json["email"] == "vertel@gmail.com"
