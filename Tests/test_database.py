from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.Connection_Through_ORM.main import app
from apps.Connection_Through_ORM.main import app
from sqlalchemy.ext.declarative import declarative_base
from apps.Connection_Through_ORM.config import settings
from apps.Connection_Through_ORM.database import get_db, Base


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
