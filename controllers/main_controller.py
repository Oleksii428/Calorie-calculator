from enums.weight_types_enum import lower, normal, over, fattiness_1, fattiness_2, fattiness_3
from enums.food_course_enum import weight_gain, weight_safe, waste


def get_recommendations(user):
    if not user:
        print("you must login first")
    else:
        imt = user["weight"] / (user["height"] ** 2)
        weight_type = ""
        food_course = ""

        if imt < 18.5:
            weight_type = lower
            food_course = weight_gain
        elif imt >= 18.5 < 25:
            weight_type = normal
            food_course = weight_safe
        elif imt >= 25 < 30:
            weight_type = over
            food_course = waste
        elif imt >= 30 < 35:
            weight_type = fattiness_1
            food_course = waste
        elif imt >= 35 < 40:
            weight_type = fattiness_2
            food_course = waste
        elif imt >= 40:
            weight_type = fattiness_3
            food_course = waste

        print(f"Ваш індекс маси тіла = {round(imt, 4)}.")
        print(f"Категорія Вашої  ваги: {weight_type}.")
        print(f"Рекомендація щодо цілей харчування: {food_course}.")

        bmr = 0
        if user["gender"] == "male":
            bmr = 88.362 + (13.397 * user["weight"]) + (4.799 * user["height"]) + (5.677 * user["age"])
        else:
            bmr = 447.593 + (9.247 * user["weight"]) + (3.097 * user["height"]) + (4.33 * user["age"])
