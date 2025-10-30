# Author - Daniel Dang
# Filename - database.py
# Purpose - To setup the database for the Tender Ledger project

import sqlite3
from .categories import add_category
from .payment_methods import add_payment_method

DB_DIR = "data"
DB_NAME = "tender_ledger.db"
DB_PATH = DB_DIR + "/" + DB_NAME

TEST_DB_NAME = "test_tender_ledger.db"
TEST_DB_PATH = DB_DIR + "/" + TEST_DB_NAME

DEFAULT_CATEGOREIS = ["Food", 
                      "Utilities", 
                      "Housing", 
                      "Healthcare",
                      "Insurance",
                      "Entertainment",
                      "Travel",
                      "Shopping",
                      "Other"]

DEFAULT_PAYMENT_METHODS = ["Cash",
                           "Credit"]

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
        set_up_categories_table(cur, con)
        set_up_payment_methods_table(cur, con)
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
                    created_at DATETIME,
                    updated_at DATETIME
                )
                """)

def set_up_categories_table(cur, con):
    """
    Create the table for the categories

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS categories(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT UNIQUE NOT NULL,
                    created_at DATETIME,
                    updated_at DATETIME,
                
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)
    
    
    # Inserting default categories
    for category in DEFAULT_CATEGOREIS:
        add_category(None, category, cur, con)

def set_up_payment_methods_table(cur, con):
    """
    Create the table for the payment methods

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """
    cur.execute("""
                CREATE TABLE IF NOT EXISTS payment_methods(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT UNIQUE NOT NULL,
                    created_at DATETIME,
                    updated_at DATETIME,
                
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)
    
    # Inserting default payment methods
    for payment_method in DEFAULT_PAYMENT_METHODS:
        add_payment_method(None, payment_method, cur, con)

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

def clear_tables(cur, con):
    """
    Empty the tables in the database

    Argument:
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """
    cur.execute("DELETE FROM expenses")
    cur.execute("DELETE FROM categories")
    cur.execute("DELETE FROM payment_methods")
    cur.execute("DELETE FROM users")

    # Leave the defaults alone
    for payment_method in DEFAULT_PAYMENT_METHODS:
        add_payment_method(None, payment_method, cur, con)
    for category in DEFAULT_CATEGOREIS:
        add_category(None, category, cur, con)
    