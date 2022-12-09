from enums.user_characteristics_enum import WEIGHT, HEIGHT, AGE, GENDER, MALE, FEMALE, NAME, PASSWORD, PHYSICAL_ACTIVITY
from enums.weight_types_enum import LOWER, NORMAL, OVER, FATTINESS_1, FATTINESS_2, FATTINESS_3
from enums.food_courses_enum import WEIGHT_GAIN, WEIGHT_SAFE, WEIGHT_WASTE
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
            food_course = WEIGHT_WASTE
        elif imt >= 30 < 35:
            weight_type = FATTINESS_1
            food_course = WEIGHT_WASTE
        elif imt >= 35 < 40:
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

        coefficient_physic_activity = 0

        match login_user[PHYSICAL_ACTIVITY]:
            case 1:
                coefficient_physic_activity = 1.375
            case 2:
                coefficient_physic_activity = 1.55
            case 3:
                coefficient_physic_activity = 1.725
            case 4:
                coefficient_physic_activity = 1.9

        daily_calorie_norm = round(bmr * coefficient_physic_activity)

        protein_min = 0
        protein_max = 0

        fats_min = 0
        fats_max = 0

        carbohydrate_min = 0
        carbohydrate_max = 0

        if food_course == WEIGHT_WASTE:
            protein_min = (daily_calorie_norm * 25) / 100
            protein_max = (daily_calorie_norm * 35) / 100

            fats_min = (daily_calorie_norm * 25) / 100
            fats_max = (daily_calorie_norm * 30) / 100

            carbohydrate_min = (daily_calorie_norm * 40) / 100
            carbohydrate_max = (daily_calorie_norm * 50) / 100
        elif food_course == WEIGHT_SAFE:
            protein_min = (daily_calorie_norm * 10) / 100
            protein_max = (daily_calorie_norm * 15) / 100

            fats_min = (daily_calorie_norm * 25) / 100
            fats_max = (daily_calorie_norm * 30) / 100

            carbohydrate_min = (daily_calorie_norm * 60) / 100
            carbohydrate_max = (daily_calorie_norm * 75) / 100
        elif food_course == WEIGHT_GAIN:
            protein_min = (daily_calorie_norm * 30) / 100
            protein_max = (daily_calorie_norm * 35) / 100

            fats_min = (daily_calorie_norm * 25) / 100
            fats_max = (daily_calorie_norm * 30) / 100

            carbohydrate_min = (daily_calorie_norm * 45) / 100
            carbohydrate_max = (daily_calorie_norm * 55) / 100

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
        print(f"Добова норма споживаних калорій: {daily_calorie_norm}.")
        print(f"Баланс білків, жирів і вуглеводів: ")
        for key in pfc:
            print(f"{key}: {pfc[key]}")

# Як розрахувати норму білків, жирів і вуглеводів?
#
# Щоденна норма БЖУ - це кількість білків, жирів і вуглеводів, необхідних для збереження балансу поживних речовин і підтримки організму в формі.
#
# Як же розрахувати свій БЖУ? Співвідношення БЖУ при схудненні залежить від кількості споживаних калорій і обчислюється в процентному співвідношенні від допустимої норми калорій. Також їх баланс залежить від того, якого ефекту ви хочете досягти.
#
# Білків - 25-35%. protein
# Жирів - 25-30%. fats
# Норма вуглеводів в день при СХУДНЕННІ - 40-50% від суми калорій. carbohydrate
#
# Ідеальним для зниження ваги дієтологи вважають таке співвідношення БЖУ: по 30% білків і жирів, а також 40% вуглеводів. Тобто, добова норма калорій набирається 30-ма відсотками білкових продуктів, 40% вуглеводів і 30% жирів.
#
# При НАБОРІ маси
# Добова норма білків - 30-35%;
# Жирів - 25-30%;
# Денна норма вуглеводів - 45-55%.
#
# При підрахунках необхідно пам'ятати, що:
# 1 грам білка і вуглеводів - це 4 калорії;
# 1 грам жиру - 9 калорій.
# Формула розрахунку БЖУ при схудненні (30% білка і жиру, 40% вуглеводів):
#
# Вуглеводи = (норма кКал Х 0,4) / 4;
# Білки = (норма кКал Х 0,3) / 4;
# Жири = (норма кКал Х 0,3) /
# Розглянемо, як розраховується БЖУ на прикладі.
#
# Таким чином, дівчина, яка бажає схуднути, з допустимим добовим коридором калорій від 1400 до 1750 кКал повинна вживати в день:
#
# Від 105 до 131 грама білків;
# Від 47 до 58 грамів жирів;
# Від 140 до 175 грамів вуглеводів.
# Ось і всі розрахунки. Якщо розібратися, нічого складного в підрахунку КБЖУ немає.
#
# Поради:
# • Незалежно від одержаних розрахунків, щодня потрібно з'їдати не менше 35 грам жирів.
# • Намагайтеся віддавати перевагу складним вуглеводам.
# • Отримана в ході розрахунків норма білка повинна складати від 0,7 до 2 грам на 1 кг вашої ваги.
# • При розрахунку КБЖУ і складанні свого щоденного меню не забувайте про основні правила правильного харчування. Тоді процес схуднення буде ще більш легким і ефективним.
#
# Якщо у вас немає часу або бажання робити підрахунки самостійно, ви можете легко провести розрахунок калорій, білків, жирів і вуглеводів (КБЖУ) за допомогою онлайн калькулятора, спеціальної програми або навіть додатку на смартфоні. В інтернеті є безліч сайтів, на яких це можна зробити швидко і безкоштовно. Меньше
