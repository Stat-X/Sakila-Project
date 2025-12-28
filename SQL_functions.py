from math import ceil
from typing import Callable, Any
from collections import defaultdict

import pymysql

import CONFIG_AND_MODULES as config
from colorama import Fore, init
import functions as f
from QueryLogger import myLogger

init(autoreset=True)


#============================================================================================================================#                                                                                                                           #
#                       This function (executor_sql) is the core of all SQL queries in the project                           #
#                     It acts as a universal executor – every query to the database goes through it                          #                                                                                                                           #
#============================================================================================================================#
def executor_sql(
        query: str,
        get_only_result:bool=False,
        actor:bool=False,
        title:bool=False,
        need_to_log:bool=True,
        search_key:str=None,
        search_value:str=None,
        **params
) -> tuple[tuple[Any, ...], ...] | None:
    """
        Executes SQL query and handles results/logging.

        Args:
            query (str): SQL query string.
            get_only_result (bool): If True, return raw DB results.
            actor (bool): Helps adjust flow for actor-specific searches.
            title (bool): Helps adjust flow for title-specific searches.
            need_to_log (bool): If True, logs query to Mongo.
            search_key/value: Info for logging.
            **params: Params for SQL placeholders — allow fine-tuning specific queries.

        Returns:
            Raw results or paginated rendering, or None on error.
    """
    try:
        with pymysql.connect(**config.DB_CONFIG_READ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                status = "Success" if results else "Failure"

                if need_to_log:
                    myLogger.extract_query_and_params(query, params)
                    myLogger.set_query_result_status(status, search_key, search_value)
                    myLogger.log_in_mongo()
                    myLogger.log_in_txt()

                if not results:
                    print(Fore.RED + "No results found.", end="\n\n")

                    if actor:
                        f.print_slowly("Try again:", Fore.RED, end="\n\n", delay=0.02)
                        return f.find_by_actor()
                    if title:
                        f.print_slowly("Try again:", Fore.RED, end="\n\n", delay=0.02)
                        return f.find_by_title()
                    return f.lets_begin()

                if get_only_result:
                    return results
                else:
                    return paginate_list(results, render_films, actor=actor)

    except (pymysql.err.OperationalError,
            pymysql.err.ProgrammingError,
            pymysql.err.InternalError,
            pymysql.err.IntegrityError,
            pymysql.err.DataError,
            pymysql.err.InterfaceError,
            pymysql.err.DatabaseError,
            Exception) as e:
        print(Fore.RED + str(e), end='\n\n')
        return f.main_menu()

#============================================================================================================================#                                                                                                                     #
#                                 Below is the first part of functions                                                       #
#                           These functions serve as templates for SQL queries                                               #                                                                                                                 #
#============================================================================================================================#

def where_search_title(where: str) -> None:
    """
        Searches films by title and fills the list with the result
        Then ,  calls the function if_not_results(result)
    """
    query = f"""{config.main_table} 
    
                SELECT
                    * 
                FROM 
                    main_table 
                WHERE title = %(where)s OR title LIKE %(like)s;
            """

    parameters_of_search = {"where": where, "like": f"%{where}%"}
    executor_sql(query, **parameters_of_search, title=True, search_key="Title", search_value=f"{where} or like %{where}%")


def where_search_specific_year(year: int) -> None:
    """
    Searches films by year and fills the list with the result

    Args:
     year(int): year to search for

    :return: None
    """
    query = f"""{config.main_table} 

                SELECT 
                    * 
                FROM 
                    main_table
                WHERE 
                    release_year = %(year)s;
            """
    parameters_of_search = {"year": year}
    executor_sql(query, **parameters_of_search, search_key="Year", search_value=str(year))


def where_search_range_year(year_1, year_2) -> None:
    query = f"""{config.main_table} 
                
                SELECT 
                    * 
                FROM 
                    main_table
                WHERE 
                    release_year BETWEEN %(year_1)s AND %(year_2)s 
                ORDER BY release_year ASC;
            """

    parameters_of_search = {"year_1": year_1, "year_2": year_2}
    executor_sql(query, **parameters_of_search, search_key="Range of years", search_value=f"between {year_1} and {year_2}")


def where_genre_year(genre, year_1=None, year_2=None) -> None:
    type_of_year = "AND release_year BETWEEN %(year_1)s AND %(year_2)s" if year_1 and year_2 else "AND release_year = %(year_1)s"
    query = f"""{config.main_table} 

                    SELECT 
                        * 
                    FROM 
                        main_table
                    WHERE 
                        genre = %(genre)s
                        {type_of_year}
                    ORDER BY release_year ASC;
                """
    params_range = {"genre": genre, "year_1": year_1, "year_2": year_2}
    params_single_year = {"genre": genre, "year_1": year_1}

    if year_1 and year_2:
        return executor_sql(query, **params_range, search_key="range of year and genre", search_value=f"between {year_1} and {year_2}, {genre}")

    return executor_sql(query, **params_single_year, search_key="year and genre",search_value=f"{year_1} and {genre}")


def where_like_actor(name) -> None:
    query = f"""{config.table_for_actors} 

                SELECT 
                    *
                FROM 
                    actors_table 
                WHERE 
                    Actor LIKE %(like)s;

            """
    parameters_of_search = {"like": f"{name}%"}
    executor_sql(query,  **parameters_of_search, actor=True, search_key="Actor", search_value=f"like %{name}%")



def where_genre() -> None:
    """
        Shows all unique genres from the database in a numbered list.

        Allows the user to:
        - Select a genre by number to view matching films
        - Navigate back to menu/search options
        - Exit the program
    """
    genres = show_all_genres()#this func prints the list with genres and then returns the dict, to operate with it further
    while True:
        option = input(Fore.GREEN + "Which genre do you want to see? ")

        if (option not in genres and option not in ["m", "s", "e"]) or not option:
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        elif option in genres:
            choice = genres[option]
            query = f"""{config.main_table}
                    SELECT 
                        * 
                    FROM
                        main_table
                    WHERE 
                    genre = %(genre)s;
                    """
            parameters_of_search = {"genre": choice}
            return executor_sql(query, **parameters_of_search, search_key="Genre", search_value=choice)

        elif option == "m":
            return f.main_menu()
        elif option == "s":
            return f.lets_begin()
        elif option == "e":
            return f.exit_program()


def show_all_genres() -> defaultdict[str, str]:
    """
        Shows all unique genres from the database in a numbered list.

        Gives the menu of choice.
        Returns the dict with the genres, so to analyse them then
    """
    query = f"""{config.main_table} 

                SELECT 
                    DISTINCT genre
                FROM 
                    main_table;
                """
    result = executor_sql(query, get_only_result=True, need_to_log=False)
    num = 1

    genres = defaultdict(str)

    print(Fore.YELLOW + "+" + "-" * 25 + "+")
    for genre in result:
        text = f"{num:>2}. {genre[0]:<18}"
        print(Fore.YELLOW + f"| {text} |")
        genres[str(num)] = genre[0]
        num += 1
    print(Fore.YELLOW + "+" + "-" * 25 + "+")
    print(Fore.GREEN + "\nOptions:")
    f.print_slowly("m - BACK TO MENU", Fore.LIGHTCYAN_EX)
    f.print_slowly("s - BACK TO SEARCH-OPTIONS", Fore.LIGHTCYAN_EX)
    f.print_slowly("e - EXIT", Fore.LIGHTCYAN_EX)
    return genres


def min_year() -> int: #in the whole DB
    query = f"""{config.main_table} 
                    SELECT 
                        release_year
                    FROM 
                        main_table
                    ORDER BY release_year ASC
                    LIMIT 1;
                """
    min_year = executor_sql(query, need_to_log=False, get_only_result=True)
    return min_year[0][0]

def max_year() -> int: #in the whole DB
    query = f"""{config.main_table} 
                        SELECT 
                            release_year
                        FROM 
                            main_table
                        ORDER BY release_year DESC
                        LIMIT 1;
                    """
    max_year = executor_sql(query, need_to_log=False, get_only_result=True)
    return max_year[0][0]

#============================================================================================================================#
#                                  Below is the second part of functions                                                     #
#                       These functions are responsible for displaying paged results                                         #
#                      and navigating user choices after query execution                                                     #
#============================================================================================================================#

def paginate_list(results: tuple[tuple[Any, ...], ...],
                  render_fn: Callable,
                  actor=False) -> None:
    """
       Displays results in pages and handles navigation.

       User selects how many items to show per page.
       Allows moving to next, previous page, or quitting.

       Args:
           results (list): list of items to display
           render_fn (Callable): function to render each page
           actor (bool): passed to render_fn to control actor display
    """
    total_rows = len(results)

    print(Fore.GREEN + f"There are {total_rows} results.")

    while True:
        page_size = input(Fore.GREEN + "How many elements per page would you like to see? ").strip()

        if not page_size:
            print(Fore.RED + "The field can't be empty.")
            continue

        if not page_size.isdigit():
            print(Fore.RED + "Page size must be an integer.")
            continue

        if page_size == "0":
            print(Fore.RED + "You can't 0 results per page!")
            continue

        if total_rows < int(page_size):
            print(Fore.RED + f"You can't get {int(page_size)} elements per page, because you only have {total_rows} rows.")
            continue

        break

    pages = ceil(total_rows / int(page_size))
    current = 0

    while True:
        start = current * int(page_size)
        end = start + int(page_size)
        print(Fore.LIGHTYELLOW_EX + f"\nShowing page {current + 1} of {pages}")
        print(Fore.WHITE + "-" * 30)
        render_fn(results[start:end], actor=actor)

        if pages == 1:
            break

        while True:
            cmd = input(Fore.YELLOW + "n - next, p - prev, q - quit: ").lower()
            if cmd not in ("n", "p", "q"):
                print(Fore.RED + "Invalid input!")
            elif cmd == "n" and current == pages - 1:
                print(Fore.RED + "The last page does not have the next page!")
            elif cmd == "p" and current == 0:
                print(Fore.RED + "The first page does not have the previous page!")
            else:
                break

        if cmd == "n" and current < pages - 1:
            current += 1
        elif cmd == "p" and current > 0:
            current -= 1
        elif cmd == "q":
            break

    # Navigation
    f.print_slowly("\n1. I want to find another film?", Fore.LIGHTCYAN_EX, delay=0.015)
    f.print_slowly("2. BACK TO MENU", Fore.LIGHTCYAN_EX, delay=0.015)
    f.print_slowly("3. EXIT", Fore.LIGHTCYAN_EX, delay=0.015)
    while True:
        option = input(Fore.LIGHTGREEN_EX + "Enter your choice: ")

        if option not in("1", "2", "3"):
            print(Fore.LIGHTRED_EX + f"Invalid choice: {option} or no option selected (x_x)")
            continue

        if option == "1":
            return f.lets_begin()
        elif option == "2":
            return f.main_menu()
        elif option == "3":
            return f.exit_program()



def render_films(films: list, actor=False):# param actor=True means that I search film by actors. Then I have only 1 actor to each film
    """
    Print film info: title, year, genre, and actors (if any).
    'actor' flag changes label to singular.

    Args:
        films (list): list of film data tuples
        actor (bool): use "Actor:" if True, else "Actors:"
    """
    for row in films:
        print(Fore.CYAN + "Title ---> ", end='')
        f.print_slowly(row[0], Fore.CYAN, delay=0.01)

        print(Fore.LIGHTMAGENTA_EX + "Year  ---> ", end='')
        f.print_slowly(str(row[1]), Fore.LIGHTMAGENTA_EX, delay=0.01)

        print(Fore.LIGHTBLUE_EX + "Genre ---> ", end='')
        f.print_slowly(row[2], Fore.LIGHTBLUE_EX, delay=0.01)

        if len(row) > 3 and row[3]:
            print()
            print("Actor:" if actor else "Actors:") # param actor=True means that I search film by actors. Then I have only 1 actor to each film
            for actor_ in row[3].split(','):
                print("\t➤ ", end='')
                f.print_slowly(actor_, Fore.LIGHTCYAN_EX, delay=0.003)
        print(Fore.WHITE + "-" * 30)
