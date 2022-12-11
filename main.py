import sys

from controllers.auth_controller import register, login, logout
from controllers.main_controller import get_details, get_recommendations, change_user_info, calorie_calculator

if __name__ == "__main__":
    while True:
        print("-----------------------------------------------------------------------------------------------------")
        action = input(
            "Enter number of action(register=1, login=2, logout=3, get user info=4, get recommendations=5, "
            "change_user_info=6, show calorie calculator = 7, exit=0): ")
        print("-----------------------------------------------------------------------------------------------------")
        match action:
            case "1":
                register()
            case "2":
                login()
            case "3":
                logout()
            case "4":
                get_details()
            case "5":
                get_recommendations()
            case "6":
                change_user_info()
            case "7":
                calorie_calculator()
            case "0":
                sys.exit()
            case _:
                print("Unknown action")
