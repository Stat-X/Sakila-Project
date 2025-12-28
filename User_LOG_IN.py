import os

from colorama import Fore, init
from dotenv import load_dotenv
from numpy.ma.core import choose

import functions as f

load_dotenv()
init(autoreset=True)

from UserStorage import UserStorage
from CONFIG_AND_MODULES import DB_CONFIG_WRITE
import Animation as anim

userStorage = UserStorage()
userStorage.create_connection(**DB_CONFIG_WRITE)
userStorage.create_database(os.getenv("DB_DATABASE_WRITE"))
userStorage.create_table(os.getenv("DB_TABLE_WRITE"))



def create_account():
    print()
    f.print_slowly("This is menu for CREATING ACCOUNT", Fore.LIGHTYELLOW_EX, delay=0.01)

    while True:
        print()
        f.print_slowly("""
1. I have already created an account!
2. BACK TO 'WELCOME-PAGE'
3. EXIT PROGRAM
        
Or give data to create a new account!
""", Fore.CYAN, delay=0.005)
        user = input(Fore.GREEN + "Create username: ").strip()
        if user == "1":
            return login_account()
        elif user == "2":
            return f.main()
        elif user == "3":
            return f.exit_program()

        if userStorage.user_already_exists(user) or len(user) < 5:
            anim.animation_spinner("Checking up of the username", time_of_loading=3)
            print(Fore.RED + "Username already exists or the username is too short(5 characters minimum)")
            continue
        break

    while True:
        password = input(Fore.GREEN +  "Create password: ").strip()
        if password == "1":
            return login_account()
        elif password == "2":
            return f.main()
        elif password == "3":
            return f.exit_program()

        if len(password) < 5:
            print(Fore.RED + "Password must be at least 5 characters")
            continue
        break

    userStorage.add_user(user, password)
    return login_account()


def login_account():
    f.print_slowly("This is menu for LOG-IN",  Fore.LIGHTYELLOW_EX, delay=0.01)

    while True:
        print()
        f.print_slowly("""
1. I still dont have an account!
2. BACK TO 'WELCOME-PAGE'
3. EXIT PROGRAM

Or give data to log in!
""", Fore.CYAN, delay=0.005)

        user = input(Fore.GREEN + "Enter username: ").strip()
        if user == '1':
            choose = input(f"""
{Fore.CYAN + 'Would you like to create an account?'}

1. Create an account
2. BACK TO 'WELCOME-PAGE'
3. EXIT PROGRAM
        
{Fore.GREEN + 'Enter your choice:'} """).lower()

            if choose == '1':
                return create_account()
            elif choose == '2':
                return f.main()
            elif choose == '3':
                userStorage.close_connection()
                return f.exit_program()

        elif user == '2':
            return f.main()
        elif user == '3':
            userStorage.close_connection()
            return f.exit_program()


        password = input(Fore.GREEN + "Enter password: ").strip()

        if password == '1':
            return create_account()
        elif password == '2':
            return f.main()
        elif password == '3':
            userStorage.close_connection()
            return f.exit_program()


        if not (userStorage.user_already_exists(user) and userStorage.password_correct(user, password)):
            anim.loading("Logging In")
            print(Fore.RED + "Invalid username or password. Try again.")
            continue
        print()
        anim.loading("Logging In")
        print(Fore.CYAN +  "The log-in succeeded! Welcome to the main menu!")
        userStorage.close_connection()
        return f.main_menu()





