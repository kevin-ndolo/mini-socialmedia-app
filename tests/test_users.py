from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base


# CREATE AN INDEPENDENT TESTING DATABASE

# Create a Testing Database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test"

# Create the Engine and Session for Testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db(): 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_db function in the app to use the Testing Database
app.dependency_overrides[get_db] = override_get_db



client = TestClient(app)

 
def test_root():
    response = client.get("/")
    print(response.json())
    print(response.json()["message"])
    assert (response.json()["message"]) == "Hello Multiverse"
    assert response.status_code == 200


def test_create_user():
    res = client.post("/users/", json={"email": "mike.jones@email.com", "password": "qwerty"})
    new_user = schemas.UserOut(**res.json())  
    assert res.status_code == 201
    assert new_user.email == "mike.jones@email.com"
    