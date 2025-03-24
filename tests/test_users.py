from fastapi.testclient import TestClient
import pytest
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


""" 
Create a TestClient
"""
# client = TestClient(app)

"""
 Create a TestClient using pytest fixtures. Utilizing yield instead of return allows us to carryout other actions before and after creating the TestClient. We then pass on the client to the test functions as an argument.
"""
# @pytest.fixture
# def client():
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#     Base.metadata.drop_all(bind=engine)

"""
 Because this is for testing purposes we want to be able to view the test db after creating the TestClient.
 So we change our code to drop and then create an new test db only when we create a new Testclient
"""

# @pytest.fixture
# def client():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
    

"""
We can configure one fixture to be dependant on another fixture. Passing the first fixture as an argument to the second fixture we can ensure that the first fixture is run before the second fixture.
Our current fixtures purpose is to return a Testclient(client). We need another fixture that will allow us to manipulate the database object when we need to. 

We will create a new fixture called session_fixture that will allow us to manipulate the database.

The naming of the fixture as session_fixture instead of just session is intentional to avoid confusion and any naming conflicts with the session object in the app.

We move the dropping and creating of the database to the session_fixture from the client fixture. This is because the session_fixture is now handling the logic of database.
Next, we going to copy the functionality  of the override_get_db function to the session_fixture.
Remember that even though the functionality we've copied comes from the function override_get_db, at the end of the day the purpose of the function is to create a new session object to interact with the database and close it once the request is done.
Also notice that we yield(return) a db object. This db object is what we use to query the database

We then pass the session_fixture as an argument to the client fixture. This will ensure that the session_fixture is run before the client fixture.

We then copy the entire override_get_db function into the client fixture. Since we have the session_fixture as a parameter to the client fixture then we no longer need db in the override_get_db function that is inside of the client, and we can go ahead and replace db with session_fixture.
Because we're calling the override_get_db function inside the client fixture, we then have to override it inside the client fixture. Hence we copy app.dependency_overrides[get_db] = override_get_db into the client fixture.

We now have access to the database object using the session_fixture, and we also have access to the client.

If we wanted to we could use the client and session_fixture at the same time in the same test. 
i.e

         def test_root(client, session_fixture):
            posts = session_fixture.query(models.Post).filter(models.Post.id == id)....
            res = client.get("/")
            print(res.json())

All in all the session_fixture will always be called first as any test that needs a client will call the client fixture which will in turn call session_fixture as it depends on it.





"""



@pytest.fixture
def session_fixture():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session_fixture):


    def override_get_db(): 
    # db = TestingSessionLocal()
        try:
            yield session_fixture
        finally:
            session_fixture.close()

    app.dependency_overrides[get_db] = override_get_db

   
    yield TestClient(app)
    




 
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
    