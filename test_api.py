from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Docker FastAPI"}

def test_hello_name():
    response = client.get("/hello/Taro")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Taro"}

def test_echo():
    response = client.post("/echo", json={"name": "Taro"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Taro"}


def test_create_item():
    response = client.post("/items", json={"name": "apple"})
    assert response.status_code == 200
    assert response.json()["name"] == "apple"

def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_item():
    create_response = client.post(
        "/items",
        json={"name": "apple"}
    )

    item_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/items/{item_id}"
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Item deleted",
        "id": item_id,
    }

def test_delete_missing_item():
    response = client.delete("/items/999999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Item not found"
    }

def test_update_item():
    create_response = client.post("/items", json={"name": "apple"})
    item_id = create_response.json()["id"]

    update_response = client.put(
        f"/items/{item_id}",
        json={"name": "orange"},
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == item_id
    assert data["name"] == "orange"
    assert data["status"] == "active"

    # ISO 8601形式の日時として解釈できることを確認
    datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))


def test_update_missing_item():
    response = client.put(
        "/items/999999",
        json={"name": "orange"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}