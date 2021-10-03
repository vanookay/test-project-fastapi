from src.tests.tests import *


@temp_db
def test_correct_create_city():
    request_data = {
        "name": "Саранск",
    }
    with TestClient(app) as client:
        response = client.post(f"{API_ROUTE}/city/", json=request_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == request_data['name']
    assert data["weather"]


def test_create_city_with_incorrect_city_name():
    request_data = {
        "name": "Саран",
    }
    with TestClient(app) as client:
        response = client.post(f"{API_ROUTE}/city/", json=request_data)
    assert response.status_code == 404
