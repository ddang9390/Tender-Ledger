# Author - Daniel Dang
# Filename - database.py
# Purpose - To setup the database for the Tender Ledger project

import sqlite3
import pandas as pd

DB_DIR = "data"
DB_NAME = "tender_ledger.db"
DB_PATH = DB_DIR + "/" + DB_NAME

TEST_DB_NAME = "test_tender_ledger.db"
TEST_DB_PATH = DB_DIR + "/" + TEST_DB_NAME

def set_up_database(testing=False):
    """
    Sets up the database for the Tender Ledger project

    Argument:
        testing (bool): If true, set up database for testing purposes
                        Else, set up database for prod
    """
    path = TEST_DB_PATH if testing else DB_PATH
    name = TEST_DB_NAME if testing else DB_NAME

    try:
        # Connect to database and create it if it doesn't exist
        con = sqlite3.connect(path)
        cur = con.cursor()

        # Build the tables if they don't exist
        set_up_users_table(cur)
        set_up_categories_table(cur)
        set_up_payment_methods_table(cur)
        set_up_expenses_table(cur)

        # Commit pending transactions to the database then close the connection
        con.commit()
        con.close()
        print("Database", name, " has been created")

    except sqlite3.Error as e:
        print(e)

def set_up_users_table(cur):
    """
    Create the table for the users

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT,
                    created_at DATETIME
                )
                """)

def set_up_categories_table(cur):
    """
    Create the table for the categories

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    created_at DATETIME,
                
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)

def set_up_payment_methods_table(cur):
    """
    Create the table for the payment methods

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS payment_methods(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    created_at DATETIME,
                
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)
    
def set_up_expenses_table(cur):
    """
    Create the table for the expenses

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount FLOAT NOT NULL,
                    date_of_purchase DATETIME NOT NULL,
                    payment_method_id INTEGER,
                    category_id INTEGER,
                    location TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
                """)



def execute_query(query):
    """
    Connects to database and executes the query generated from
    translating the user's sentence. Displays the results of the
    query and the generated query

    Argument:
        query (string): The generated query
    """
    con = sqlite3.connect(DB_PATH)
    print(DB_PATH)
    results = pd.read_sql_query(query, con)
    con.close()

    print("\n----Query Results----")
    if results.empty:
        print("The query produced no results")
    else:
        print(results.to_string(index=False))

    print("\nResulting Query: ", query, "\n")

    return query, results.to_html()

