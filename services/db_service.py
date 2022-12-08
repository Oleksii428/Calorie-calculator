import json


def read_db():
    with open('./data_base/db.json') as db:
        db = json.load(db)
        return db


def write_db(data):
    with open('./data_base/db.json', "w") as file:
        json.dump(data, file)


def read_login_user():
    with open('./data_base/login_user.json') as login_user:
        login_user = json.load(login_user)
        return login_user


def write_login_user(user):
    with open('./data_base/login_user.json', "w") as file:
        json.dump(user, file)
