import pytest
import jwt
from app import schemas
from app.config import settings


 
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


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('hello123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 403),
    ('hello123@gmail.com', None, 403)
])

# Test incorrect login without parametrize
# def test_incorrect_login(client, test_user):
#   res = client.post('/login', data={"username":test_user["email"], "password":"wrongPassword"})
#   print(res)
#   assert res.status_code == 403
#   assert res.json().get('detail') == 'Invalid Credentials'



# Test incorrect login with parametrize
def test_incorrect_login(client, test_user, email, password, status_code):
  res = client.post('/login', data={"username":email, "password":password})
  print(res)
  assert res.status_code == status_code