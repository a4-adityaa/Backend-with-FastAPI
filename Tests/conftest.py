from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.Connection_Through_ORM.main import app
from apps.Connection_Through_ORM.main import app
from sqlalchemy.ext.declarative import declarative_base
from apps.Connection_Through_ORM.config import settings
from apps.Connection_Through_ORM.database import get_db, Base
from apps.Connection_Through_ORM.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def Session():
    # run our code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(Session):
    def override_get_db():
        try:
            yield Session
        finally:
            Session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "aditya121@gmail.com",
                 "password":"password123"}

    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers ={
        **client.headers, "Authorization": f"Bearer {token}"
    }
    return client