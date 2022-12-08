def isUserExists(data_base, name):
    for user in data_base:
        if user["name"] == name:
            return user
