from enums.table_enum import FOOD_NAME, PROTEIN, FATS, CARBOHYDRATE, ENERGY
from enums.user_characteristics_enum import WEIGHT, HEIGHT, AGE, GENDER, MALE, FEMALE, NAME, PASSWORD, \
    PHYSICAL_ACTIVITY, PRODUCTS
from enums.weight_types_enum import LOWER, NORMAL, OVER, FATTINESS_1, FATTINESS_2, FATTINESS_3
from enums.food_courses_enum import WEIGHT_GAIN, WEIGHT_SAFE, WEIGHT_WASTE
from middlewares.user_middleware import is_user_exists
from services.db_service import read_login_user, read_db, write_db, write_login_user, read_food
from validators.auth_validator import password_validator, float_validator, int_validator, gender_validator
from prettytable import PrettyTable


def get_details():
    login_user = read_login_user()

    if not login_user:
        print("You must login first")
    else:
        for key in login_user:
            if key != NAME and key != PASSWORD:
                print(f"Your {key}: {login_user[key]}")


def change_user_info():
    login_user = read_login_user()
    user_info = login_user.copy()
    user_info.pop(NAME)

    if not login_user:
        print("You must login first")
    else:
        change_characteristic = input(f"Select what you want to change: {', '.join(user_info)}, or back: ")

        if change_characteristic == "back":
            return

        while change_characteristic not in login_user:
            print("Invalid characteristic")
            change_characteristic = input(f"Select what you want to change: {', '.join(user_info)}: ")

        new_value = 0

        if change_characteristic == PASSWORD:
            new_value = password_validator()
        elif change_characteristic == WEIGHT:
            new_value = float_validator(WEIGHT)
        elif change_characteristic == HEIGHT:
            new_value = float_validator(HEIGHT)
        elif change_characteristic == AGE:
            new_value = int_validator(AGE)
        elif change_characteristic == GENDER:
            new_value = gender_validator()
        elif change_characteristic == PHYSICAL_ACTIVITY:
            new_value = int_validator(PHYSICAL_ACTIVITY)

        db = read_db()
        for index, user in enumerate(db):
            if user[NAME] == login_user[NAME]:
                db[index][change_characteristic] = new_value
                write_db(db)
                write_login_user(db[index])
                print("Changes complete")
                break


def get_recommendations():
    login_user = read_login_user()

    if not login_user:
        print("You must login first")
    else:
        imt = login_user[WEIGHT] / ((login_user[HEIGHT] / 100) ** 2)
        weight_type = ""
        food_course = ""

        if imt < 18.5:
            weight_type = LOWER
            food_course = WEIGHT_GAIN
        elif 18.5 <= imt < 25:
            weight_type = NORMAL
            food_course = WEIGHT_SAFE
        elif 25 <= imt < 30:
            weight_type = OVER
            food_course = WEIGHT_WASTE
        elif 30 <= imt < 35:
            weight_type = FATTINESS_1
            food_course = WEIGHT_WASTE
        elif 35 <= imt < 40:
            weight_type = FATTINESS_2
            food_course = WEIGHT_WASTE
        elif imt >= 40:
            weight_type = FATTINESS_3
            food_course = WEIGHT_WASTE

        bmr = 0

        if login_user[GENDER] == MALE:
            bmr = 88.362 + (13.397 * login_user[WEIGHT]) + (4.799 * login_user[HEIGHT]) + (
                    5.677 * login_user[AGE])
        elif login_user[GENDER] == FEMALE:
            bmr = 447.593 + (9.247 * login_user[WEIGHT]) + (3.097 * login_user[HEIGHT]) + (4.33 * login_user[AGE])

        coefficient_physical_activity = 0

        match login_user[PHYSICAL_ACTIVITY]:
            case 1:
                coefficient_physical_activity = 1.375
            case 2:
                coefficient_physical_activity = 1.55
            case 3:
                coefficient_physical_activity = 1.725
            case 4:
                coefficient_physical_activity = 1.9

        daily_calorie_norm = round(bmr * coefficient_physical_activity)

        protein_min = 0
        protein_max = 0

        fats_min = 0
        fats_max = 0

        carbohydrate_min = 0
        carbohydrate_max = 0

        if food_course == WEIGHT_WASTE:
            daily_calorie_norm = daily_calorie_norm * 0.85

            protein_min = daily_calorie_norm * 0.25
            protein_max = daily_calorie_norm * 0.35

            fats_min = daily_calorie_norm * 0.25
            fats_max = daily_calorie_norm * 0.3

            carbohydrate_min = daily_calorie_norm * 0.4
            carbohydrate_max = daily_calorie_norm * 0.5
        elif food_course == WEIGHT_SAFE:
            protein_min = daily_calorie_norm * 0.1
            protein_max = daily_calorie_norm * 0.15

            fats_min = daily_calorie_norm * 0.25
            fats_max = daily_calorie_norm * 0.3

            carbohydrate_min = daily_calorie_norm * 0.6
            carbohydrate_max = daily_calorie_norm * 0.75
        elif food_course == WEIGHT_GAIN:
            daily_calorie_norm = daily_calorie_norm * 1.15

            protein_min = daily_calorie_norm * 0.3
            protein_max = daily_calorie_norm * 0.35

            fats_min = daily_calorie_norm * 0.25
            fats_max = daily_calorie_norm * 0.3

            carbohydrate_min = daily_calorie_norm * 0.45
            carbohydrate_max = daily_calorie_norm * 0.55

        pfc = {
            "protein": f"from {round(protein_min)} to {round(protein_max)}",
            "fats": f"from {round(fats_min)} to {round(fats_max)}",
            "carbohydrate": f"from {round(carbohydrate_min)} to {round(carbohydrate_max)}"
        }

        print(f"Ваш індекс маси тіла = {round(imt, 4)}.")
        print(f"Категорія Вашої  ваги: {weight_type}.")
        print(f"Рекомендація щодо цілей харчування: {food_course}.")
        if food_course == LOWER:
            print(
                "Увага! Найважливіше для тих, хто бажає схуднути - менше калорій, ніж потрібно для базового обміну "
                "речовин, вживати не можна. Так людина не худне, а завдає непоправної шкоди здоров'ю!!!"
            )
        print(f"Добова норма споживаних калорій: {round(daily_calorie_norm)}.")
        print(f"Баланс білків, жирів і вуглеводів: ")
        for key in pfc:
            print(f"{key}: {pfc[key]}")


def get_key(food):
    number = int(input("Enter number of product: "))
    key = list(food.keys())[number - 1]
    return key


def calorie_calculator():
    login_user = read_login_user()

    if not login_user:
        print("You must login first.")
    else:
        table = PrettyTable()
        table.field_names = ["№", FOOD_NAME, ENERGY, PROTEIN, FATS, CARBOHYDRATE]
        food = read_food()
        n = 1
        for key in food:
            table.add_row([n, key, *food[key].values()])
            n += 1
        print(table)

        login_user = read_login_user()
        user_products = login_user[PRODUCTS]

        user_table = PrettyTable()
        user_table.field_names = ["№", FOOD_NAME, ENERGY, PROTEIN, FATS, CARBOHYDRATE]
        h = 1
        for product in user_products:
            name = list(product.keys())[0]
            user_table.add_row([h, name, *product[name].values()])
            h += 1
        if user_table.rows:
            print("Your table:")
            print(user_table)
        else:
            print("Your table is empty")

        wanna_add = input("Do you want to add product in to your table? (y or n): ")
        while wanna_add == "y":
            number = get_key(food)
            user_table.add_row([h, number, *food[number].values()])
            h += 1

            db = read_db()
            l_user = is_user_exists(db, login_user[NAME])
            for index, user in enumerate(db):
                if user[NAME] == l_user[NAME]:
                    l_user[PRODUCTS].append({number: food[number]})
                    db[index] = l_user
                    break
            write_db(db)

            login_user[PRODUCTS].append({number: food[number]})
            write_login_user(login_user)

            print(user_table)
            wanna_add = input("Do you want to add product in to your table? (y or n): ")
