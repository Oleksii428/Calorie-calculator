from enums.user_characteristics_enum import NAME


def isUserExists(data_base, name):
    for user in data_base:
        if user[NAME] == name:
            return user
