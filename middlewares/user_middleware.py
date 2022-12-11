from enums.user_characteristics_enum import NAME


def is_user_exists(data_base, name):
    for user in data_base:
        if user[NAME] == name:
            return user
