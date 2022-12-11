import json


def read_db():
    with open('./data_base/db.json') as db:
        db = json.load(db)
        return db


def write_db(data):
    with open('./data_base/db.json', "w") as db:
        json.dump(data, db)


def read_food():
    with open('./data_base/food.json') as food:
        food = json.load(food)
        return food


def write_food(data):
    with open('./data_base/food.json', "w") as food:
        json.dump(data, food)


def read_login_user():
    with open('./data_base/login_user.json') as login_user:
        login_user = json.load(login_user)
        return login_user


def write_login_user(user):
    with open('./data_base/login_user.json', "w") as file:
        json.dump(user, file)
