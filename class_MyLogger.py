from datetime import datetime
import pathlib

from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    ConfigurationError,
    OperationFailure,
    PyMongoError
)

from colorama import Fore, init
init(autoreset=True)
import functions as f


class MyLogger:
    """
    Handles MongoDB logging for SQL queries:
    - Connects to MongoDB
    - Stores search history
    - Logs latest query and result
    - Supports top-5 most frequent searches
    """
    NOW = datetime.now().replace(microsecond=0)

    def __init__(self) -> None:
        self.client_mongo = None
        self.db = None
        self.collection = None
        self.state_collection = None #only to check whether the history of search is empty or not
        self.max_docs_in_collection = None
        self.last_query_filetxt_path = None
        self.last_query = None
        self.last_params_of_query = None
        self.key_of_search = None  # e.g. "genre"
        self.value_of_search = None #e.g. "drama"
        self.result_status = None # Success if "result found" else Failure

    def connect_mongo(self, link) -> None:
        """Connect to MongoDB using the given URI."""
        try:
            client = MongoClient(link, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            self.client_mongo = client
        except (
                ConnectionFailure,
                ServerSelectionTimeoutError,
                ConfigurationError,
                OperationFailure,
                PyMongoError,
                Exception
        ) as e:
            print(Fore.RED + f"""MongoDB connection error: {e}
That means - you won't be able to have a search history.
You can work without it, or you can solve the issue and rerun the script.""")
            print()
            return None

    def create_db(self, db_name) -> None:
        """Create MongoDB database."""
        if self.client_mongo is not None:
            self.db = self.client_mongo[db_name]

    def create_collection(self, collection_name) -> None:
        """Create MongoDB collection."""
        if self.db is not None:
            self.collection = self.db[collection_name]

    def limit_control_collection(self):
        current_count_collectoin = self.collection.count_documents({})
        if current_count_collectoin > self.max_docs_in_collection:
            oldest_doc = self.collection.find_one(sort=[("_id", 1)])
            self.collection.delete_one({"_id": oldest_doc["_id"]})
        return None

    def create_collection_of_states(self, collection_name) -> None:
        """Create MongoDB collection of states.

        This collection has only one DOCUMENT,
        which contains the info about the cleaning history.

        If cleaned == 1 ---> history of search cleaned and you cant see it.

        Each session creates its own state_collection and regulates state "cleaned"
        """
        if self.db is not None:
            self.state_collection = self.db[collection_name]
            data_cleaned_dict = {"cleaned":1 if self.data_is_cleaned() else 0}
            self.state_collection.insert_one(data_cleaned_dict)

    def state_switcher(self, data_cleaned=False) -> None:
        """
        Switches the state in the state_collection
        (if the connection to MongoDB is successful)

        Each time when a user cleans the history -> "cleaned": 1
        Each time when a user finds something -> "cleaned": 0
        """
        if self.collection is not None:
            if data_cleaned:
                self.state_collection.update_one({}, {"$set": {"cleaned": 1}}, upsert=True)
            else:
                self.state_collection.update_one({}, {"$set": {"cleaned": 0}}, upsert=True)

    def clean_history_of_search(self) -> None:
        """
        Clear the entire search history.

        - Deletes all documents from the MongoDB collection.
        - Empties the local .txt file storing the last query.
        - Updates the state to mark history as cleaned.
        - Returns to the main menu.
        """
        if self.last_query_filetxt_path is not None:
            with open(self.last_query_filetxt_path, "w") as file:
                pass
        if self.collection is not None:
            self.collection.delete_many({})
            self.state_switcher(data_cleaned=True)
            return f.main_menu()

    def clean_state_collection_before_exit(self) -> None:
        """
        Cleans the state collection before exit, so we always update
        the state_collection and see which state is at the moment of running the script.
        """
        if self.state_collection is not None:
            self.state_collection.delete_many({})

    def data_is_cleaned(self) -> bool | None:
        """
        Checks whether the cleaned history is still valid.
        """
        if self.collection is not None:
            is_empty = self.collection.find_one() is None
            if is_empty:
                return True

    def set_max_docs_in_collection(self, max_) -> None:
        """
        sets the maximum number of documents in the collection of logging
        """
        if self.collection is not None:
            self.max_docs_in_collection = max_

    def set_query_result_status(self, result_status, search_key, search_value) -> None:
        """
        collects the data of the query from executor(), to add it to a log-document in MongoDB
        """
        self.result_status = result_status
        self.key_of_search = search_key
        self.value_of_search = search_value

    def extract_query_and_params(self, query: str, params: dict) -> None:
        """
        With this we can see a pure query , how it would look like in SQL.
        This function separates also  parameters so we can see the keys of serach
        """
        from QueryLogger import pure_query #this is the main function which does a pure query from the raw one
        query = pure_query(query, params)
        self.last_query = query
        self.last_params_of_query = params

    def set_path_for_last_query(self, path, filename) -> None:
        """
         Sets the full file path where the last query result will be saved.

         Arguments:
             path (str): Path to an existing directory.
             filename (str): Name of the file to be used.

         If the path doesn't exist or is not a directory, it prints an error and exits.
         Otherwise, it saves the full path (directory + filename) to self.last_query_filetxt_path.

         Note: This does not create the file, just prepares the full path.
        """
        try:
            path = pathlib.Path(path).expanduser().resolve()

            if not path.exists():
                print(Fore.RED + f"Directory for logging the last query does not exist: {path}. Set your path correctly.")
                print()
                return

            if not path.is_dir():
                print(Fore.RED + f"Path is not a directory: {path}")
                return

            full_path = path / filename

            self.last_query_filetxt_path = full_path

            if not full_path.exists():
                full_path.touch()


        except Exception as e:
            print(Fore.RED + f"Error while processing the path: {e}")


    def log_in_txt(self):
        if self.last_query is not None:
            try:
                with open(self.last_query_filetxt_path, "w",  encoding="utf-8", newline='') as file:
                    file.write(str(self.last_query))
            except Exception as e:
                print(Fore.RED + "Error while saving the last query  ", e)
                return


    def get_last_query(self) -> None:
        """
        Retrieves the last query from the last_query_filetxt_path.
        :return: None
        """
        if self.last_query_filetxt_path is not None:
            try:
                with open(self.last_query_filetxt_path, "r",encoding="utf-8", newline='') as file:
                    file_content = file.read()
                    if not file_content:
                        print(Fore.RED + "You have no last query yet.")
                        return f.main_menu()
                    f.print_slowly(file_content, Fore.LIGHTBLUE_EX, delay=0.01)
                    return f.main_menu()
            except FileNotFoundError as e:
                print(Fore.RED + str(e))
            except Exception as e:
                print(Fore.RED + str(e))

    def log_in_mongo(self) -> None:
        """
        Save the latest SQL query and its metadata to MongoDB.

        - Formats the query using sqlparse.
        - Enforces max document limit via external helper.
        - Stores time, query, search key/value, and result status.
        - Updates state to mark history as not cleaned.
        """
        if self.collection is not None:
            import sqlparse

            self.limit_control_collection()

            doc_to_save_inMongo = {
                "time": MyLogger.NOW,
                "query": sqlparse.format(self.last_query, reindent=True, keyword_case='upper'),
                "key of search": self.key_of_search,
                "value of search": self.value_of_search,
                "Result of the searching": self.result_status
            }
            self.collection.insert_one(doc_to_save_inMongo)
            self.state_switcher(data_cleaned=False)

    def top_queries(self, limit) -> None:
        """
        Display the top 5 most frequent search keys and their most used values.

        - Aggregates queries by "key of search" and counts frequency.
        - For each key, finds the most common "value of search".
        - Prints each as a readable search description.
        - Returns to the main menu after displaying.
        """
        if self.collection is not None:
            if self.data_is_cleaned():
                print(Fore.RED + "The search history is empty!")
                return f.main_menu()

            top_values = list(self.collection.aggregate([
                {"$group": {"_id": "$value of search", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]))

            print()
            print(Fore.LIGHTYELLOW_EX + f"Top {limit} most popular queries:")
            num = 1
            for value_item in top_values:
                value = value_item["_id"]

                top_values = list(self.collection.aggregate([
                    {"$match": {"value of search": value}},
                    {"$limit": 1}
                ]))

                if top_values:
                    key = top_values[0].get("key of search", "unknown")
                    print(f"→ {num}. {Fore.LIGHTYELLOW_EX + 'Find a film where'} {Fore.CYAN + key} {Fore.LIGHTYELLOW_EX + 'is'} {Fore.CYAN + value}")
                    num += 1
                else:
                    print(f"→ Find a film where {key} has unknown value")

            return f.main_menu()

        print(Fore.RED + "There is an issue with the MongoDB connection, we can't show you the most popular queries!")
        return f.main_menu()


    def execute_last_query(self) -> None:
        """
            Executes the most recent SQL query saved in a local text file.

            Function workflow:
            - Reads the last SQL query from `self.last_query_filetxt_path`.
            - Displays the query in a readable, styled format using `f.print_slowly`.
            - Asks the user whether they want to execute this query again.
            - If the user confirms ('1'), the query is executed via `executor_sql`.
            - If the user declines ('0'), the program returns to the main menu.
            - Invalid inputs are handled with a prompt until a valid option is entered.

        """
        from SQL_functions import executor_sql
        from CONFIG_AND_MODULES import main_table
        with open(self.last_query_filetxt_path, "r",encoding="utf-8", newline='') as file:
            text = file.read()
            your_last_query = text
            full_query = f"{main_table} {text} \n"
            print(Fore.GREEN + "Your last query is: ", end="\n\n")
            f.print_slowly(your_last_query, Fore.LIGHTBLUE_EX, delay=0.01, end="\n\n")

            while True:
                choice = input(Fore.LIGHTBLUE_EX + "Do you want to execute the last query?(1 - Yes, 0 - No) ").strip()
                if choice not in ("1", "0"):
                    print(Fore.LIGHTRED_EX + f"Invalid choice: {choice} or no option selected (x_x)")
                    continue
                elif choice == "1":
                    executor_sql(full_query, need_to_log=False)
                    return f.main_menu()
                elif choice == "0":
                    return f.main_menu()






















