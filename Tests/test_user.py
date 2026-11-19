from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.Connection_Through_ORM.main import app
from apps.Connection_Through_ORM.main import app
from sqlalchemy.ext.declarative import declarative_base
from apps.Connection_Through_ORM.config import settings
from apps.Connection_Through_ORM import schemas


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()





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