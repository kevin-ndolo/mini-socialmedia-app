import pytest
import jwt
from app import schemas
from app.config import settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "steve.jobs@email.com",
                 "password": "qwerty"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


 
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
    

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200