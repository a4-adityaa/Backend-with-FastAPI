from fastapi.testclient import TestClient
from apps.Connection_Through_ORM.main import app
from apps.Connection_Through_ORM import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hey how are you?'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users",json={"email":"aadi12334@gmail.com", "password":"aadi1234"})
    new_user = schemas.UserOut(**res.json())  # unpacking the new user data
    assert new_user.email == "aadi12334@gmail.com"
    assert res.status_code ==201