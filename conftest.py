import pytest
import sqlite3

from project import create_app, db

@pytest.fixture()
def app():
    # create sqlite databse in memory for testing
    # database creater b4 / destroyed after every single test
    app = create_app("sqlite://") 

    with app.app_context():
        db.create_all()

    # $ pytest -s (to print out this statement)
    #print("CREATING TEMPORARY DATABASE")
    
    #anything before yielding = setup of the test
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def session():
    connection = sqlite3.connect(":memory:")
    db_session = connection.cursor()
    db_session.execute(
        "CREATE TABLE IF NOT EXIST  \
        tempToDo(                   \
            ID INTEGER PRIMARY KEY, \
            Name STRING,            \
            Description STRING,     \
            Image STRING,           \
            Status STRING,          \
            AddOn STRING,           \
            Category INTEGER        \
        )"
    )
    db_session.commit()
    yield db_session
    connection.close()




