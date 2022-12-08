from enums.user_characteristics_enum import WEIGHT, HEIGHT, AGE, GENDER, MALE, FEMALE, NAME, PASSWORD
from enums.weight_types_enum import LOWER, NORMAL, OVER, FATTINESS_1, FATTINESS_2, FATTINESS_3
from enums.food_courses_enum import WEIGHT_GAIN, WEIGHT_SAFE, WASTE
from services.db_service import read_login_user


def get_details():
    login_user = read_login_user()

    for key in login_user:
        if key != NAME and key != PASSWORD:
            print(f"Your {key}: {login_user[key]}")


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
        elif imt >= 18.5 < 25:
            weight_type = NORMAL
            food_course = WEIGHT_SAFE
        elif imt >= 25 < 30:
            weight_type = OVER
            food_course = WASTE
        elif imt >= 30 < 35:
            weight_type = FATTINESS_1
            food_course = WASTE
        elif imt >= 35 < 40:
            weight_type = FATTINESS_2
            food_course = WASTE
        elif imt >= 40:
            weight_type = FATTINESS_3
            food_course = WASTE

        print(f"Ваш індекс маси тіла = {round(imt, 4)}.")
        print(f"Категорія Вашої  ваги: {weight_type}.")
        print(f"Рекомендація щодо цілей харчування: {food_course}.")

        bmr = 0
        if login_user[GENDER] == MALE:
            bmr = 88.362 + (13.397 * login_user[WEIGHT]) + (4.799 * login_user[HEIGHT]) + (
                        5.677 * login_user[AGE])
        elif login_user[GENDER] == FEMALE:
            bmr = 447.593 + (9.247 * login_user[WEIGHT]) + (3.097 * login_user[HEIGHT]) + (4.33 * login_user[AGE])
