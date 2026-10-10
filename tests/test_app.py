import pytest
from app import app, members

@pytest.fixture()
def client():
    app.config["TESTING"]=True
    members.clear()
    with app.test_client() as client:
        yield client
    members.clear()

def test_home(client):
    r=client.get("/")
    assert r.status_code==200
    assert r.get_json()["application"]=="ACEest Fitness & Gym"

def test_health(client):
    assert client.get("/health").get_json()=={"status":"healthy"}

def test_members_empty(client):
    assert client.get("/members").get_json()==[]

def test_add_member(client):
    r=client.post("/members",json={"name":"Rohit","age":33,"plan":"annual"})
    assert r.status_code==201
    data=r.get_json()
    assert data["id"]==1
    assert data["name"]=="Rohit"
    assert data["age"]==33

def test_invalid_member(client):
    assert client.post("/members",json={"name":"Rohit"}).status_code==400
    assert client.post("/members",json={"name":"Rohit","age":"abc"}).status_code==400

def test_get_member(client):
    client.post("/members",json={"name":"Rohit","age":33})
    assert client.get("/members/1").get_json()["name"]=="Rohit"

def test_missing_member(client):
    assert client.get("/members/999").status_code==404

def test_delete_member(client):
    client.post("/members",json={"name":"Rohit","age":33})
    assert client.delete("/members/1").status_code==200
    assert client.get("/members/1").status_code==404
