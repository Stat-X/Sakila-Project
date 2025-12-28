import os

import sqlparse
from dotenv import load_dotenv
load_dotenv()

import CONFIG_AND_MODULES as config
from class_MyLogger import MyLogger


myLogger = MyLogger()

myLogger.connect_mongo(os.getenv("MONGO"))
myLogger.create_db(os.getenv("DB_MONGO"))
myLogger.create_collection(os.getenv("COLLECTION_MONGO"))
myLogger.create_collection_of_states(os.getenv("COLLECTION_MONGO_STATES"))
myLogger.set_path_for_last_query(os.getenv("FILE_LAST_QUERY"), "last_query.txt")
myLogger.set_max_docs_in_collection(24) #25 in fact


def pure_query(query: str, params: dict) -> None:
    """
    Prepare a SQL query string by inserting parameters safely.

    - Adds quotes around string values in params.
    - Tries to insert params into the query string.
    - If formatting fails, prints an error and returns None.
    - Removes certain table name placeholders from the query.
    - Formats the query for better readability (uppercase keywords, indentation).

    Returns the cleaned and formatted query as a string for saving.
    Returns None if there was a formatting error.
    """
    from functions import main_menu
    safe_params = {
        k: f"'{v}'" if isinstance(v, str) else v
        for k, v in params.items()
    }
    try:
        query = query % safe_params
    except Exception as e:
        print("SQL formatting error:", e)
        return main_menu()

    if config.table_for_actors in query:
        query = query.replace(config.table_for_actors, "")
    elif config.main_table in query:
        query = query.replace(config.main_table, "")

    query =  sqlparse.format(query.strip(), reindent=True, keyword_case='upper')
    return query















