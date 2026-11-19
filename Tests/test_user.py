from fastapi.testclient import TestClient
from apps.Connection_Through_ORM.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hey how are you?'
    assert res.status_code == 200