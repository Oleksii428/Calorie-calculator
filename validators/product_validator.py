import re


def title_validator():
    while True:
        product_title = input("Enter product name: ")

        if re.match(r"^[a-zA-Z]{2,15}$", product_title):
            return product_title.title()
        else:
            print("Name not valid. Only letters. Min: 2, max: 15.")


def epfc_validator(characteristic):
    while True:
        data = input(f"Enter {characteristic}/100g of product: ")
        try:
            data = float(data)
        except ValueError:
            print(f"{characteristic} not valid. Only int or float.")
        else:
            if data < 0.1 or data > 5000:
                print(f"{characteristic} not valid(min: 1, max: 5000).")
            else:
                return float(data)


def number_validator(characteristic, max_number):
    while True:
        data = input(f"Enter {characteristic}: ")

        if not data.isdigit():
            print(f"{characteristic} not valid(only int).")
            continue
        elif 1 <= int(data) <= max_number:
            return int(data)
        else:
            print(f"Product with {characteristic} {data} not found.")
