import sys
import time

from colorama import Fore, init
init(autoreset=True)


import CONFIG_AND_MODULES as config
from QueryLogger import myLogger



def print_slowly(text: str,
                 color: str,
                 delay: float=0.03,
                 end="\n") -> None:
    """
    Print the given text slowly with specified color in the terminal.

    Parameters:
        :param text: (str): The text to print.
        :param color: (str) ANSI color code string (e.g., Fore.GREEN).
        :param delay: (float, optional) Delay between printing each character in seconds
        :param end:  for the regulation of the basic "end" in print()
    """
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(end=end)


def main():
    """
    Initializes the session by recording the start time in the global variable `begin`,
    prints welcome messages then calls and returns the main menu function.
    """
    from User_LOG_IN import create_account, login_account
    print()
    global begin
    begin = time.perf_counter()
    print_slowly(f"""
    Welcome to ICH!
    My name is {config.DB_CONFIG_READ['database']}!
    
    DO YOU HAVE AN ACCOUNT, OR YOU WANT TO CREATE ONE?
    1. Create an account
    2. I have one
    3. EXIT
    """, Fore.CYAN, delay=0.016)
    print_slowly("\t(￣▽￣)ノ", Fore.LIGHTYELLOW_EX, delay=0.015)
    print()
    while True:
        choice = input(Fore.GREEN + "Choose an option: ").strip()
        print()

        if choice not in ("1", "2", "3"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {choice} or no option selected (x_x)")
            continue

        if choice == "1":
            return create_account()
        elif choice == "2":
            return login_account()
        elif choice == "3":
            return exit_program()


def main_menu() -> None:
    """
    Show main menu, get user input, and call related functions.
    Returns result of called function or None.

    Repeats menu on invalid input.
    """
    print(Fore.WHITE + "=" * 120, end='')
    # ===================MENU========================================
    print(Fore.GREEN + "\nMain Menu:")
    print_slowly("1. Who are you?",Fore.LIGHTCYAN_EX, delay=0.01)
    print_slowly("2. Lets begin our work with films!", Fore.LIGHTCYAN_EX, delay=0.01)
    print_slowly("3. Show me previous query", Fore.LIGHTCYAN_EX, delay=0.01)
    print_slowly("4. Show me TOP N queries", Fore.LIGHTCYAN_EX, delay=0.01)
    print_slowly("5. Delete the entire history of search", Fore.LIGHTCYAN_EX, delay=0.01)
    print_slowly("6. EXIT", Fore.LIGHTCYAN_EX, delay=0.01)
    # ===================================================================
    while True:
        option = input(Fore.LIGHTGREEN_EX + "Enter your choice: ").strip()

        if option not in ("1", "2", "3", "4", "5", "6"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        elif option == "1":
            return who_are_you_answer()
        elif option == "2":
            return lets_begin()
        elif option == "3":
            return myLogger.execute_last_query()

        elif option == "4":
            while True:
                try:
                    top_n = int(input(Fore.GREEN + "How many TOP N would you like to see? : "))

                    if top_n <= 0:
                        print(Fore.LIGHTRED_EX + "The input should be greater than 0 (x_x)")
                        continue

                    return myLogger.top_queries(top_n)

                except ValueError:
                    print(Fore.LIGHTRED_EX + f"Invalid choice: it should be a number (x_x)")
                except Exception as e:
                    print(Fore.LIGHTRED_EX + f"Invalid choice: {e} (x_x)")

        elif option == "5":
            return delete_history_of_search()
        elif option == "6":
            return exit_program()


def who_are_you_answer() -> None:
    """
        Display the 'who are you' answer  and show options menu.
        Calls functions based on user input.

        Global:
             answer_who_are_you_str -- string with the answer text.

        Repeats menu on invalid input.
    """
    print(Fore.WHITE + "=" * 120, end='')
    global answer_who_are_you_str
    print_slowly(answer_who_are_you_str, Fore.CYAN, delay=0.005)
    print(Fore.WHITE + "=" * 120, end='')
    # ===================OPTIONS========================================
    print(Fore.GREEN + "\nOptions:")
    print_slowly("1. Lets begin our work with films?", Fore.LIGHTCYAN_EX)
    print_slowly("2. BACK TO MENU", Fore.LIGHTCYAN_EX)
    print_slowly("3. EXIT",Fore.LIGHTCYAN_EX)
    # ===================================================================
    while True:
        option = input(Fore.LIGHTGREEN_EX + "Enter your choice: ").strip()

        if option not in ("1", "2", "3"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        elif option == "1":
            return lets_begin()
        elif option == "2":
            return main_menu()
        elif option == "3":
            return exit_program()

answer_who_are_you_str = f"""
       My name is {config.DB_CONFIG_READ['database']}

       I am a database from an SQL server. I can help you with searching of films drawing on:
       
       ➤ genres
       ➤ year
       ➤ actors

       Also I can show the most favourite queries
       Besides, everything you send me is logged and I can show you the previous queries"""


def lets_begin() -> None:
    """
    Display film search options menu and call functions based on user choice.
    Repeats menu on invalid input.
    """
    print(Fore.WHITE + "=" * 120, end='')
    # ===================OPTIONS========================================
    print(Fore.GREEN + "\nFilm-Search Options:")
    print_slowly("1. Find a film by title?",Fore.LIGHTCYAN_EX,delay=0.005)
    print_slowly("2. Find a film by year?",Fore.LIGHTCYAN_EX,delay=0.005)
    print_slowly("3. Find a film by actors?",Fore.LIGHTCYAN_EX,delay=0.005)
    print_slowly("4. Find a film by genre?",Fore.LIGHTCYAN_EX,delay=0.005)
    print_slowly("5. Find a film by genre and year?", Fore.LIGHTCYAN_EX, delay=0.005)
    print_slowly("6. BACK TO MENU",Fore.LIGHTCYAN_EX,delay=0.005)
    print_slowly("7. EXIT",Fore.LIGHTCYAN_EX,delay=0.005)
    # ===================================================================
    while True:
        option = input(Fore.LIGHTGREEN_EX + "Enter your choice: ").strip()

        if option not in ("1", "2", "3", "4", "5", "6", "7"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        elif option == "1":
            return find_by_title()
        elif option == "2":
            return find_by_years()
        elif option == "3":
            return find_by_actor()
        elif option == "4":
            return find_by_genre()
        elif option == "5":
            return find_genre_year()
        elif option == "6":
            return main_menu()
        elif option == "7":
            return exit_program()


def find_by_title() -> None:
    """
    Prompt user to enter a film title (or part of it) or choose an option.
    Calls relevant functions based on input.
    Repeats prompt if no input.
    """
    from SQL_functions import where_search_title
    print(Fore.WHITE + "=" * 120, end='')
    # ===================OPTIONS========================================
    print(Fore.GREEN + "\nOptions:")
    print_slowly("1. BACK TO MENU", Fore.LIGHTCYAN_EX)
    print_slowly("2. BACK TO SEARCH-OPTIONS", Fore.LIGHTCYAN_EX)
    print_slowly("3. EXIT", Fore.LIGHTCYAN_EX)
    # ===================================================================
    while True:
        option = input(Fore.GREEN + "Give me a title or part of it or choose the option: ").strip()
        print("\n")

        if not option:
            print(Fore.LIGHTRED_EX + "No option selected! (x_x)")
            continue

        elif option in ("1", "2", "3"):
            print(Fore.LIGHTCYAN_EX + f"""You chose {option}?
1. Did you mean the command '{commands[option]["description"]}',
2. or you just wanted to find a film by '{option}'""")
            while True:
                clarification = input(Fore.GREEN + 'Enter your choice: ').strip()
                if clarification not in ("1", "2"):
                    print(Fore.LIGHTRED_EX + f"Invalid choice or no option selected (x_x)")
                    continue

                elif clarification == "1":
                    return commands[option]["func"]()
                elif clarification == "2":
                    return where_search_title(option)

        return where_search_title(option)


def find_by_years(return_year_only:bool=False) -> None:
    """
    User chooses to search films by year or range.

    - 'Y': enter a single year  search that year.
    - 'R': enter start & end year  search in range.
    - Validates input (digits, year bounds, logic).
    - Options to go back or exit.

    """
    from SQL_functions import min_year, max_year
    print(Fore.WHITE + "=" * 120, end='')
    # ===================OPTIONS========================================
    print(Fore.GREEN + "\nOptions:")
    print_slowly("1. BACK TO MENU", Fore.LIGHTCYAN_EX)
    print_slowly("2. BACK TO SEARCH-OPTIONS", Fore.LIGHTCYAN_EX)
    print_slowly("3. EXIT", Fore.LIGHTCYAN_EX)
    # ===================================================================
    while True:
        print(Fore.LIGHTRED_EX + f"Remember, that year must be between {min_year()} and {max_year()}")
        option = input(Fore.GREEN + f"Print {Fore.LIGHTYELLOW_EX + 'R'} {Fore.GREEN + 'if you want a range of years or'} {Fore.LIGHTYELLOW_EX + 'Y'} {Fore.GREEN + 'if you want a specific year:'}").lower().strip()
        if option not in ("1", "2", "3", "r", "y"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue
        elif option == "r":
            return find_year_range(return_year_only=return_year_only)
        elif option == "y":
            return find_specific_year(return_year_only=return_year_only)
        elif option == "1":
            return main_menu()
        elif option == "2":
            return lets_begin()
        elif option == "3":
            return exit_program()



def find_year_range(return_year_only:bool=False) -> None | int:
    """
         Prompt the user to enter a valid film year.

         Checks:
         - Input must be digits only.
         - Year must be within allowed range (min_year to max_year).

         Args:
             return_year_only (bool):
                 If True, returns the year as int.
                 If False, performs SQL search for that year and returns result.

         Returns:
             int or query result depending on return_year_only.
    """
    from SQL_functions import min_year, max_year
    from SQL_functions import where_search_range_year
    while True:
        try:
            year_1_input = input(Fore.GREEN + "Give me the first year of the range: ").strip()
            year_2_input = input(Fore.GREEN + "Give me the second year of the range: ").strip()

            if not (year_1_input.isdigit() and year_2_input.isdigit()):
                raise ValueError(Fore.LIGHTRED_EX + "Only digits are allowed!")

            year_1 = int(year_1_input)
            year_2 = int(year_2_input)

            if year_1 < min_year() or year_2 > max_year():
                raise ValueError(Fore.LIGHTRED_EX + f"The year must be between {min_year()} and {max_year()}!")

            if year_1 >= year_2:
                raise ValueError(Fore.LIGHTRED_EX + "Second year must be greater than the first!")

            return where_search_range_year(year_1, year_2) if not return_year_only else (year_1, year_2)

        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)


def find_specific_year(return_year_only:bool=False) -> None | int:
    """
     Prompt the user to enter a valid film year.

     Checks:
     - Input must be digits only.
     - Year must be within allowed range (min_year to max_year).

     Args:
         return_year_only (bool):
             If True, returns the year as int.
             If False, performs SQL search for that year and returns result.

     Returns:
         int or query result depending on return_year_only.
     """
    from SQL_functions import min_year, max_year
    from SQL_functions import where_search_specific_year
    while True:
        try:
            year_input = input(Fore.GREEN + "Give me the year of the film: ").strip()

            if not (year_input.isdigit()):
                raise ValueError(Fore.LIGHTRED_EX + "Only digits are allowed!")

            year = int(year_input)

            if year not in range(min_year(), max_year() + 1):
                raise ValueError(Fore.LIGHTRED_EX + f"The year must be between {min_year()} and {max_year()}!")

            return where_search_specific_year(year) if not return_year_only else year
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)


def find_genre_year():
    """
     Lets the user pick a genre and then choose a year or range of years to find films.

     Steps:
     - Shows all available genres.
     - User selects a genre by number.
     - User decides if they want to search by a specific year or a range.
     - Calls SQL query with chosen genre and year
     - Supports special commands(but only on the stage of genre choosing)
         * 'm' to go back to main menu,
         * 's' to go back to film search menu,
         * 'e' to exit the program.

     Returns:
         Result of the SQL query or triggers menu navigation/exit.
     """
    from SQL_functions import min_year, max_year
    from SQL_functions import show_all_genres,where_genre_year
    print()
    print(Fore.GREEN + "Here are all genres which you can find. And after you can choose a year!")
    genres = show_all_genres() #this func prints the list with genres and then returns the dict, to operate with it further
    while True:
        option = input(Fore.GREEN + "Which genre do you want to see? ")
        print()

        if (option not in genres and option not in ["m", "s", "e"]) or not option:
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        if option in genres:
            choice = genres[option]

            print(Fore.GREEN + "Now, choose a year!")
            print(Fore.LIGHTRED_EX + f"Remember, that year must be between {min_year()} and {max_year()}", end="\n\n")

            while True:
                option = input(Fore.GREEN + f"Print {Fore.LIGHTYELLOW_EX + 'R'} {Fore.GREEN + 'if you want a range of years or'} {Fore.LIGHTYELLOW_EX + 'Y'} {Fore.GREEN + 'if you want a specific year:'}").lower().strip()
                if option not in ("r", "y"):
                    print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
                    continue
                elif option == "r":
                    year_1, year_2 = find_year_range(return_year_only=True)
                    return where_genre_year(choice, year_1, year_2)
                elif option == "y":
                    year = find_specific_year(return_year_only=True)
                    return where_genre_year(choice, year)

        #choices bellow work only while you are choosing a genre
        elif option == "m":
            return main_menu()
        elif option == "s":
            return lets_begin()
        elif option == "e":
            return exit_program()


def find_by_actor() -> None:
    """
    Asks user for actor's name (or part of it) to search films.

    - Validates input (not empty, not digits).
    - Allows user to go back to menu/options or exit.
    - Passes input to SQL.where_like_actor().
    """
    from SQL_functions import where_like_actor
    print(Fore.WHITE + "=" * 120, end='')
    # ===================OPTIONS========================================
    print(Fore.GREEN + "\nOptions:")
    print_slowly("1. BACK TO MENU", Fore.LIGHTCYAN_EX)
    print_slowly("2. BACK TO SEARCH-OPTIONS", Fore.LIGHTCYAN_EX)
    print_slowly("3. EXIT", Fore.LIGHTCYAN_EX)
    # ===================================================================

    while True:
        name = input(Fore.GREEN + "Give me the actor's name or the part of it: ").strip()

        if not name:
            print(Fore.LIGHTRED_EX + "The field cannot be empty!")
            continue

        elif name.isdigit() and name not in ("1", "2", "3"):
            print(Fore.LIGHTRED_EX + "The input should NOT be a number (except of menu options)!")
            continue

        if name == "1":
            return main_menu()
        elif name == "2":
            return lets_begin()
        elif name == "3":
            return exit_program()

        return where_like_actor(name)


def find_by_genre() -> None:
    """
       Shows all available genres using SQL.show_all_genres().
       And  show_all_genres() is also responsible for searching
    """
    from SQL_functions import where_genre
    print()
    print(Fore.GREEN + "Here are all genres which you can find:")
    return where_genre()


def delete_history_of_search() -> None:
    """
     Asks user for confirmation to delete search history.

    - If confirmed (1), deletes history via myLogger.
    - If canceled (0), returns to menu.
    - Handles invalid input.
    - Warns if MongoDB is not connected.
    """
    while True:
        if myLogger.collection is not None:
            choice = input(Fore.RED + "Are you sure you want to delete the history(1 - Yes, 0 - No)? ").strip()

            if choice not in ("1", "0"):
                print(Fore.LIGHTRED_EX + f"Invalid choice: {choice} or no option selected (x_x)")
                continue

            elif choice == "1":
                print_slowly("The history of the search has been deleted.", Fore.RED, delay=0.01)
                myLogger.clean_history_of_search()
            elif choice == "0":
                return main_menu()

        print(Fore.RED + "There is an issue with MongoDB connection. You don't have access to the history!")
        return main_menu()


def exit_program() -> None:
    """
    Calculates and displays session duration.
    Print a thank-you message with duration in minutes and seconds.
    Then exit the program.
    """
    from User_LOG_IN import userStorage
    session_duration = time.perf_counter() - begin
    minutes = int(session_duration // 60)
    seconds = session_duration % 60


    text = f"""
    Thank you for using ICH!
    The program has been completed successfully!.
    
    The session lasted {minutes} minutes and {round(seconds)} seconds.
    """
    print(Fore.WHITE + "=" * 120, end='')
    print_slowly(text, Fore.CYAN, delay=0.009)

    userStorage.close_connection()
    myLogger.clean_state_collection_before_exit()

    print_slowly("\t(￢‿￢)", Fore.LIGHTYELLOW_EX, delay=0.015)
    print(Fore.WHITE + "=" * 120, end='')

    sys.exit(0)


commands = { #it is used only for function find_by_title

    "1": {"func": main_menu, "description": "BACK TO MENU"},
    "2": {"func": lets_begin, "description": "BACK TO SEARCH-OPTIONS"},
    "3": {"func":exit_program, "description": "EXIT"}
}




