import re

from enums import HEIGHT, WEIGHT, AGE, PHYSICAL_ACTIVITY, MALE, FEMALE


def name_validator():
    while True:
        name = input("Enter name: ")

        if re.match(r"^[a-zA-Z]{2,15}$", name):
            return name.title()
        else:
            print("Name not valid. Only letters. Min: 2, max: 15.")


def password_validator():
    while True:
        password = input("Enter password: ")

        if re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%_*#?&])[A-Za-z\d@$!%_*#?&]{4,}$", password):
            return password
        else:
            print("Password not valid. Minimum 4 characters, at least 1 letter, 1 number and 1 special character.")


def float_validator(characteristic):
    while True:
        data = input(f"Enter {characteristic}: ")
        try:
            data = float(data)
        except ValueError:
            print(f"{characteristic} not valid. Only int or float.")
        else:
            if characteristic == WEIGHT and data <= 14 or data > 200:
                print(f"{characteristic} not valid(min: 20 kg, max: 200).")
            elif characteristic == HEIGHT and data <= 67 or data > 251:
                print(f"{characteristic} not valid(min: 100 sm, max: 250 sm).")
            else:
                return float(data)


def int_validator(characteristic):
    while True:
        data = input(f"Enter {characteristic}: ")

        if characteristic == AGE:
            if not data.isdigit():
                print(f"{characteristic} not valid(only int, min: 1, max: 120).")
                continue
            elif 1 <= int(data) <= 120:
                return int(data)
            else:
                print(f"{characteristic} not valid(only int, min: 1, max: 120).")
        if characteristic == PHYSICAL_ACTIVITY:
            if not data.isdigit():
                print("")
                print(f"{characteristic} not valid(only int, min: 1, max: 4).")
                continue
            elif 1 <= int(data) <= 4:
                return int(data)
            else:
                print(f"{characteristic} not valid(only int, min: 1, max: 4).")
        else:
            print(f"{characteristic} not valid.")


def gender_validator():
    while True:
        gender = input("Enter gender: ").lower()

        if gender == MALE or gender == FEMALE:
            return gender.lower()
        else:
            print("gender invalid(male or female).")
