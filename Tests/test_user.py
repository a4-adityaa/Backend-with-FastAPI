from apps.Connection_Through_ORM import schemas
from jose import jwt
from apps.Connection_Through_ORM import schemas
from .test_database import client, Session
import pytest
from apps.Connection_Through_ORM.config import settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "aditya121@gmail.com",
                 "password":"password123"}

    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hey how are you?'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json={"email":"aadi12334@gmail.com", "password":"aadi1234"})
    new_user = schemas.UserOut(**res.json())  # unpacking the new user data
    assert new_user.email == "aadi12334@gmail.com"
    assert res.status_code ==201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,  settings.secret_key , algorithms= [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200