# file name to start with "test_"
from project.models import User
import responses
import flask,sqlite3
from flask import url_for,redirect
import pytest

def test_home(client):
    response = client.get("/")
    # expected output
    assert b"<title>Home</title>" in response.data

#app is passed in as an argument to check data in the database
def test_register(client,app):
    #client sent post request to register route
    response = client.post("/register",data={"email":"register@test.com","password":"testregister"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "register@test.com"


def test_login(client,app):
    client.post("/register",data={"email":"login@test.com","password":"testlogin"})
    response = client.post("/login",data={"email":"login@test.com","password":"testlogin"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "login@test.com"

def test_invalid_login(client):
    # no register statement, hence user does not exist
    client.post("/login",data={"email":"login@test.com","password":"testlogin"})
    response = client.get("/display")
    # 401 is error that user gets trying to access the page
    # without succesful login 
    assert response.status_code == 401

def test_logout(client):
    client.post("/register",data={"email":"login@test.com","password":"testlogin"})
    client.post("/login",data={"email":"login@test.com","password":"testlogin"})
    response = client.get("/logout")
    assert b"Redirecting" in response.data

def test_display(client):
    client.post("/register",data={"email":"login@test.com","password":"testlogin"})
    client.post("/login",data={"email":"login@test.com","password":"testlogin"})
    response = client.get("/display")
    assert b"<head><title>Todo List</title></head>" in response.data

###########################################################################################################################################################################
# ARCHIVES


# def test_add(client,app):
#     client.post("/register",data={"email":"login@test.com","password":"testlogin"})
#     client.post("/login",data={"email":"login@test.com","password":"testlogin"})
#     with app.app_context():
#         client.post(
#             "/add",
#             data = {
#                 "categoryID":1,
#                 "description":"testtask",
#                 "status":"Pending",
#                 "addOn":"2023-10-09 01:17:25.555152",
#                 "photo":"test.png",
#                 "filename":"test.png"
#             }
#         )
#         response = client.get("/display")
#         assert b"testtask" in response.data



# def test_edit(client,app):
#     client.post("/register",data={"email":"login@test.com","password":"testlogin"})
#     client.post("/login",data={"email":"login@test.com","password":"testlogin"})
#     client.post(
#         "/edit",
#         data={
#             "itemID":"22",
#             "description":"test3"
#             }  
#     )
#     response = client.get("/display")
#     assert b"..." in response.data


# @responses.activate
# def test_get_file(client,mocker,monkeypatch,app):
#     # responses.add(
#     #     # arg 01: type of request method
#     #     responses.GET,
#     #     # arg 02: url u wanna mock
#     #     url_for("flask.send_from_directory"),
#     #     # arg 03: specified return json response
#     #     json={"filename":'test.png'},
#     #     status=200
#     # )

#     csv = "/uploads/test.csv"
#     csv_data = open(csv, "rb")
#     data = {
#         "categoryID":1,
#         "description":"feed cat",
#         "photo":(csv_data,"test.csv")
#     }
    
#     client.post(
#         #form action
#         url_for('main.process_add'),
#         data=data,
#         buffered=True,
#         content_type="multipart/form-data",
#     )

#     # create user
#     client.post("/register",data={"email":"login@test.com","password":"testlogin"})
#     client.post("/login",data={"email":"login@test.com","password":"testlogin"})

#     # mock and add test file to temporary database
#     client.post("/process/add",)
#     response = client.get("/photos/<filename>",data={"filename":"test.png"})

#     # check if image is returned
#     with app.app_context():
#         assert b"test.png" in response.data






    
