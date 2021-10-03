import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database

from src.db.database import Base
from src.main import app
from src.services.general import get_db

client = TestClient(app)

API_ROUTE = '/api/v1'


@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."

    # Create test database and tables
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield SessionLocal

    # Drop the test database
    drop_database(TEST_SQLALCHEMY_DATABASE_URL)


def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        # Sessionmaker instance to connect to test DB
        #  (SessionLocal)From fixture

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        # get to use SessionLocal received from fixture_Force db change
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_Undo db
        app.dependency_overrides[get_db] = get_db

    return func
