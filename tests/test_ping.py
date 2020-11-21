def test_ping(test_app):
    ''' Check health status of main application '''
    response = test_app.get("/ping/")
    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong",
        "environment": "development"
    }
