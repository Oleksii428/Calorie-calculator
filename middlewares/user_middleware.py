import json

from enums import NAME


def is_user_exists(data_base, name):
    for user in data_base:
        if user[NAME] == name:
            return user


def is_user_login():
    with open('./data_base/login_user.json') as login_user:
        login_user = json.load(login_user)
    return login_user
