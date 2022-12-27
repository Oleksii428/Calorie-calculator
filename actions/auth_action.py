from enums import NAME, WEIGHT, HEIGHT, AGE, PHYSICAL_ACTIVITY, GENDER, PASSWORD, PRODUCTS
from services import read_db, write_db, write_login_user
from middlewares import is_user_exists, is_user_login
from validators import name_validator, password_validator, float_validator, int_validator, gender_validator


def register():
    db = read_db()

    name = name_validator()
    while is_user_exists(db, name):
        print(f"user with name {name} is already exist")
        name = name_validator()

    password = password_validator()
    weight = float_validator(WEIGHT)
    height = float_validator(HEIGHT)
    age = int_validator(AGE)
    gender = gender_validator()
    physical_activity = int_validator(PHYSICAL_ACTIVITY)

    new_user = {
        NAME: name,
        PASSWORD: password,
        WEIGHT: weight,
        HEIGHT: height,
        AGE: age,
        GENDER: gender,
        PHYSICAL_ACTIVITY: physical_activity,
        PRODUCTS: []
    }

    db.append(new_user)
    write_db(db)

    print("New user has been created")


def login():
    db = read_db()
    login_user = is_user_login()
    if login_user:
        print(f"User {login_user[NAME]} is already login. You need to logout first")
        return
    elif not db:
        print(f"You need to register first")
        return

    user_name = input("Enter name: ").title()

    user = is_user_exists(db, user_name)

    while not user:
        print(f"user with name {user_name} not found")
        user_name = input("Enter name again: ").title()
        user = is_user_exists(db, user_name)

    user_password = input("Enter password: ")

    while user[PASSWORD] != user_password:
        print("wrong password")
        user_password = input("Enter password again: ")

    write_login_user(user)
    print(f"Welcome, {user_name}!")


def logout():
    login_user = is_user_login()

    if login_user:
        write_login_user({})
        print(f"Goodbye, {login_user[NAME]}!")
    else:
        print("Not login user")
