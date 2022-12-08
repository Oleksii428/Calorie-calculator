import json


def readDb():
    with open('db.json') as db:
        db = json.load(db)
        return db


def writeDb(data):
    with open('db.json', "w") as file:
        json.dump(data, file)
