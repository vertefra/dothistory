import json
from project.app.schemas import authors


def test_create_author(test_app_with_db):

    payload = authors.AuthorRequestPayload(
        name="Test Name",
        email="Test Email",
        password="Test Password"
    )

    print(payload.dict())

    response = test_app_with_db.post(
        '/authors/', data=json.dumps(payload.dict()))
    print(response)

    assert response.status_code == 201
    assert type(response) == authors.AuthorResponsePayload
