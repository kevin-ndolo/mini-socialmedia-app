from app import schemas
from .database import client, session_fixture
 
def test_root(client):
    response = client.get("/")
    print(response.json())
    print(response.json()["message"])
    assert (response.json()["message"]) == "Hello Multiverse"
    assert response.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "mike.jones@email.com", "password": "qwerty"})
    new_user = schemas.UserOut(**res.json())  
    assert res.status_code == 201
    assert new_user.email == "mike.jones@email.com"
    