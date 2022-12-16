from prettytable import PrettyTable

from enums import *
from middlewares import *
from services import read_food, read_db, write_db, write_login_user, write_food
from validators import number_validator, title_validator, epfc_validator


def get_action():
    action = input(
        "[Calorie Calculator] Enter number of an action: show your table=1, add product to your table=2, "
        "remove product from your table=3, create new "
        "product=4, show main table=5, back to main menu=0: ")
    return action


def print_table():
    table = PrettyTable()
    table.field_names = ["№", f"{FOOD_NAME}-g", f"{ENERGY}/100g", f"{PROTEIN}/100g", f"{FAT}/100g",
                         f"{CARBOHYDRATE}/100g"]
    food = read_food()

    n = 1
    for key in food:
        table.add_row([n, key, *food[key].values()])
        n += 1
    print(table)


def calorie_calculator():
    login_user = is_user_login()

    if not login_user:
        print("You must login first.")
        return

    print_table()
    food = read_food()

    login_user = is_user_login()
    user_products = login_user[PRODUCTS]

    user_table = PrettyTable()
    user_table.field_names = ["№", f"{FOOD_NAME}-g", f"{ENERGY}/100g", f"{PROTEIN}/100g", f"{FAT}/100g",
                              f"{CARBOHYDRATE}/100g"]

    action = get_action()

    while action != "0":
        match action:
            case "1":
                if not user_products:
                    print("Your table is empty")
                else:
                    new_user_table = PrettyTable()
                    new_user_table.field_names = ["№", f"{FOOD_NAME}-g", f"{ENERGY}/100g", f"{PROTEIN}/100g",
                                                  f"{FAT}/100g",
                                                  f"{CARBOHYDRATE}/100g"]
                    energy_sum = 0
                    protein_sum = 0
                    fat_sum = 0
                    carbohydrate_sum = 0

                    h = 1
                    for product in user_products:
                        name = list(product.keys())[0]

                        energy_sum += product[name][ENERGY]
                        protein_sum += product[name][PROTEIN]
                        fat_sum += product[name][FAT]
                        carbohydrate_sum += product[name][CARBOHYDRATE]

                        new_user_table.add_row([h, name, *product[name].values()])
                        h += 1

                    new_user_table.add_row(
                        ["*", "Sum", f"{round(energy_sum, 1)}", f"{round(protein_sum, 1)}", f"{round(fat_sum, 1)}",
                         f"{round(carbohydrate_sum, 1)}"])
                    print(new_user_table)
                    print(energy_sum)

                action = get_action()
            case "2":
                max_number = 0
                for _ in food:
                    max_number += 1
                number = number_validator("Number of product", max_number)
                food_title = list(food.keys())[number - 1]

                is_product_exists = False

                for product in user_products:
                    if list(product.keys())[0].startswith(food_title):
                        is_product_exists = True

                if not is_product_exists:
                    weight = int(input("Enter weight of product (g): "))
                    h = 0
                    user_table.add_row(
                        [h, f"{food_title}-{weight}",
                         *[round(i / 100 * weight, 1) for i in food[food_title].values()]]
                    )
                    h += 1

                    db = read_db()
                    l_user = is_user_exists(db, login_user[NAME])
                    for index, user in enumerate(db):
                        if user[NAME] == l_user[NAME]:
                            for value in food[food_title]:
                                food[food_title][value] = round((food[food_title][value] / 100) * weight, 1)
                            l_user[PRODUCTS].append({f"{food_title}-{weight}": food[food_title]})
                            db[index] = l_user
                            break
                    write_db(db)

                    login_user[PRODUCTS].append({f"{food_title}-{weight}": food[food_title]})
                    write_login_user(login_user)
                    print(f"Product {food_title} has been added to your table")
                else:
                    print("This product already in your table")

                action = get_action()

            case "3":
                if not user_table.rows:
                    print("Your table is empty")
                else:
                    max_number = 0
                    for _ in food:
                        max_number += 1
                    number = number_validator("Number of product", max_number)

                    db = read_db()
                    l_user = is_user_exists(db, login_user[NAME])
                    delete_product = list(l_user[PRODUCTS][number - 1].keys())[0]
                    l_user[PRODUCTS].pop(number - 1)
                    write_db(db)

                    login_user[PRODUCTS].pop(number - 1)

                    write_login_user(login_user)
                    print(f"Product {delete_product} has been deleted")

                action = get_action()
            case "4":
                product_title = title_validator()
                energy = epfc_validator(ENERGY)
                protein = epfc_validator(PROTEIN)
                fat = epfc_validator(FAT)
                carbohydrate = epfc_validator(CARBOHYDRATE)

                food[product_title] = {ENERGY: energy, PROTEIN: protein, FAT: fat,
                                       CARBOHYDRATE: carbohydrate}

                new_table = PrettyTable()
                new_table.field_names = ["№", f"{FOOD_NAME}-g", f"{ENERGY}/100g", f"{PROTEIN}/100g", f"{FAT}/100g",
                                         f"{CARBOHYDRATE}/100g"]
                write_food(food)
                food = read_food()
                n = 1
                for key in food:
                    new_table.add_row([n, key, *food[key].values()])
                    n += 1
                print(new_table)
                print(f"Product {product_title} has been added to main table")

                action = get_action()
            case "5":
                print_table()

                action = get_action()
            case _:
                print("Unknown command")

                action = get_action()
