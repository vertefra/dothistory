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
        name="entry3",
        email="email3@gmail.com",
        password="pass"
    )

    test_client = test_app_with_db.TestClient

    resp_1 = test_client.post(
        "/authors/", data=json.dumps(payload_1.dict())
    )

    resp_2 = test_client.post(
        "/authors/", data=json.dumps(payload_2.dict())
    )

    resp_3 = test_client.post(
        "/authors/", data=json.dumps(payload_3.dict())
    )

    assert resp_1.status_code == 201
    assert resp_2.status_code == 201
    assert resp_3.status_code == 201

    response = test_client.get("/authors/")

    assert response.status_code == 200

    response_dict = response.json()

    assert type(response_dict) == list
    assert response_dict[0]["name"] == "entry1"
    assert response_dict[1]["name"] == "entry2"
    assert response_dict[2]["name"] == "entry3"
    assert response_dict[0]["password"] is None


def test_find_author_by_id(test_app_with_db):

    test_client = test_app_with_db.TestClient

    payload_1 = authors.AuthorRequestPayload(
        name="entry1",
        email="email1@gmail.com",
        password="pass"
    )

    resp_1 = test_client.post("/authors/", data=json.dumps(payload_1.dict()))

    assert resp_1.status_code == 201

    response = test_client.get(f"/authors/{1}")

    response_dict = response.json()

    assert response_dict["name"] == "entry1"
    assert response_dict["email"] == "email1@gmail.com"
    assert "password" not in response_dict.values()


def test_update_author(test_app_with_db):

    test_client = test_app_with_db.TestClient

    payload_1 = authors.AuthorRequestPayload(
        name="entry1",
        email="email1@gmail.com",
        password="pass"
    )

    resp_1 = test_client.post("/authors/", data=json.dumps(payload_1.dict()))

    assert resp_1.status_code == 201

    resp_dict = resp_1.json()
    id = resp_dict["id"]

    updated_payload = authors.AuthorRequestPayload(
        name="updated name",
        email="updated@email.com",
        password="updated pass"
    )

    # print("should look for entry with id == ", id)

    response = test_client.put(
        f"/authors/{id}", data=json.dumps(updated_payload.dict())
    )

    assert response.status_code == 203

    response = test_client.get(f"/authors/{id}")

    assert response.status_code == 200

    response_dict = response.json()

    assert response_dict["name"] == "updated name"
    assert response_dict["email"] == "updated@email.com"
    assert "password" not in response_dict.keys()


def test_update_author_not_found(test_app_with_db):
    test_client = test_app_with_db.TestClient

    updated_payload = authors.AuthorRequestPayload(
        name="updated name",
        email="updated@email.com",
        password="updated pass"
    )

    id = 99

    response = test_client.put(
        f"/authors/{id}", data=json.dumps(updated_payload.dict())
    )

    assert response.status_code == 404

    response_dict = response.json()

    assert response_dict["detail"] == "Author not found"
