import pytest

from app import app, members


@pytest.fixture(autouse=True)
def reset_members():
    members.clear()
    yield
    members.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["application"] == "ACEest Fitness & Gym"


def test_ui(client):
    response = client.get("/ui")
    assert response.status_code == 200
    assert b"Application is running successfully." in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_members_empty(client):
    response = client.get("/members")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_member(client):
    payload = {"name": "Alice", "age": 28, "plan": "premium"}
    response = client.post("/members", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Alice"
    assert data["age"] == 28
    assert data["plan"] == "premium"


def test_get_member(client):
    client.post("/members", json={"name": "Bob", "age": 30})
    response = client.get("/members/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Bob"


def test_delete_member(client):
    client.post("/members", json={"name": "Charlie", "age": 25})
    response = client.delete("/members/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "member deleted"
    assert client.get("/members").get_json() == []


def test_delete_member_not_found(client):
    response = client.delete("/members/999")
    assert response.status_code == 404


def test_add_member_invalid(client):
    response = client.post("/members", json={"name": "Dana"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "name and age are required"


def test_add_member_bad_age(client):
    response = client.post("/members", json={"name": "Eve", "age": "abc"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "age must be an integer"
    response = client.post("/members", json={"name": "Eve", "age": 0})
    assert response.status_code == 400
    assert response.get_json()["error"] == "age must be greater than 0"


def test_get_member_not_found(client):
    response = client.get("/members/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "member not found"