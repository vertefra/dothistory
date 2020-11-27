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
    assert type(response_json["id"]) == int
    assert response_json["name"] == "Test Name"
    assert response_json["email"] == "vertel@gmail.com"


def test_duplicate_mail_fails(test_app_with_db):

    payload_1 = authors.AuthorRequestPayload(
        name="entry1",
        email="email@gmail.com",
        password="pass"
    )

    payload_2 = authors.AuthorRequestPayload(
        name="entry2",
        email="email@gmail.com",
        password="pass"
    )

    test_client = test_app_with_db.TestClient

    resp_1 = test_client.post(
        "/authors/", data=json.dumps(payload_1.dict()))

    assert resp_1.status_code == 201

    resp_2 = test_client.post(
        "/authors/", data=json.dumps(payload_2.dict())
    )

    assert resp_2.status_code == 400


def test_find_all_authors(test_app_with_db):

    payload_1 = authors.AuthorRequestPayload(
        name="entry1",
        email="email1@gmail.com",
        password="pass"
    )

    payload_2 = authors.AuthorRequestPayload(
        name="entry2",
        email="email2@gmail.com",
        password="pass"
    )

    payload_3 = authors.AuthorRequestPayload(
        name="entry2",
        email="email3@gmail.com",
        password="pass"
    )

    test_client = test_app_with_db.TestClient

    resp_1 = test_client.post(
        "/authors/", data=json.dumps(payload_1.dict()))

    resp_2 = test_client.post(
        "/authors/", data=json.dumps(payload_2.dict()))

    resp_3 = test_client.post(
        "/authors/", data=json.dumps(payload_3.dict()))

    assert resp_1.status_code == 201
    assert resp_2.status_code == 201
    assert resp_3.status_code == 201

    response = test_client.get("/authors/")

    assert response.status_code == 200

    response_dict = response.json()

    assert type(response_dict) == list
