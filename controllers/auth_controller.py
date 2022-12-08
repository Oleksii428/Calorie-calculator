from services.db_service import readDb, writeDb
from middlewares.user_middleware import isUserExists


def register():
    db = readDb()

    name = input("Enter name: ")
    password = input("Enter password: ")
    weight = float(input("Enter weight: "))
    height = float(input("Enter height: "))
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    physical_activity = int(input("Enter level of physical activity (min: 1, max: 4): "))

    new_user = {
        "name": name,
        "password": password,
        "weight": weight,
        "height": height,
        "age": age,
        "gender": gender,
        "physical_activity": physical_activity
    }

    if not isUserExists(db, new_user["name"]):
        db.append(new_user)

        writeDb(db)

        print("New user has been created")
    else:
        print(f"user with name {new_user['name']} is already exist")


def login():
    user_name = input("Enter name: ")

    db = readDb()

    user = isUserExists(db, user_name)

    if not user:
        print(f"user with name {user_name} not found")
    else:
        user_password = input("Enter password: ")

        if user["password"] == user_password:
            print(user)
            return user
        else:
            print("wrong password")
