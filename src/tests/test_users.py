from src.tests.tests import *


@temp_db
def test_correct_create_user():
    request_data = {
        "surname": "ivanov",
        "name": "Darth",
        "age": 18
    }
    with TestClient(app) as client:
        response = client.post(f"{API_ROUTE}/users/", json=request_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["surname"] == "ivanov"
    assert data["name"] == "Darth"
    assert data["age"] == 18


@temp_db
def test_create_user_without_parameter():
    request_data = {
        "surname": "ivanov",
        "name": "Darth",
    }
    with TestClient(app) as client:
        response = client.post(f"{API_ROUTE}/users/", json=request_data)
    assert response.status_code == 422
