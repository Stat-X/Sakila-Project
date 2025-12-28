import sys
import time
from typing import Callable

import pymysql

from colorama import Fore, init

import functions

init(autoreset=True)

from functools import wraps
import Animation as anim

#decorator
def try_exeption(func: Callable) -> Callable:
    @wraps(func) #to save metadata of an original function
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (pymysql.err.OperationalError,
            pymysql.err.ProgrammingError,
            pymysql.err.InternalError,
            pymysql.err.IntegrityError,
            pymysql.err.DataError,
            pymysql.err.InterfaceError,
            pymysql.err.DatabaseError,
            Exception) as e:
            print(Fore.LIGHTRED_EX + "The issue is with SQL. You can not continue without correct connection. Please try again later.")
            print(Fore.RED + str(e), end='\n\n')
            sys.exit(1)
    return wrapper


class UserStorage:

    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.database = None
        self.conn = None
        self.cursor = None
        self.user_session_path = None

    @try_exeption
    def create_connection(self, host=None, port=None, user=None, password=None) -> None:
        anim.animation_spinner("Connection to the Database...")
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password)
        self.cursor = self.conn.cursor()

    @try_exeption
    def create_database(self, database:str) -> None:
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        self.conn.commit()
        self.database = database

    @try_exeption
    def create_table(self, table:str) -> None:
        self.cursor.execute(f"USE {self.database};")
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)
        self.conn.commit()
        self.table = table

    @try_exeption
    def add_user(self, username:str, password:str) -> None:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(sql, (username, password))
        self.conn.commit()
        print()
        print(Fore.GREEN + "User inserted successfully")

    @try_exeption
    def user_already_exists(self, username: str) -> bool:
        sql = "SELECT 1 FROM users WHERE BINARY username = %s LIMIT 1"
        self.cursor.execute(sql, (username,))
        return self.cursor.fetchone() is not None

    @try_exeption
    def password_correct(self, user: str, password: str) -> bool:
        sql = "SELECT password FROM users WHERE BINARY username = %s LIMIT 1"
        self.cursor.execute(sql, (user,))
        result = self.cursor.fetchone()
        if result is None:
            return False

        stored_password = result[0]
        return stored_password == password

    @try_exeption
    def close_connection(self) -> None:
        if self.cursor:
            try:
                self.cursor.close()
            except Exception:
                pass
        if self.conn:
            try:
                self.conn.close()
                functions.print_slowly("Connection to the UserStorage closed successfully!", Fore.LIGHTGREEN_EX, delay=0.01)
            except Exception:
                pass
        print()











