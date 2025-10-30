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

class DatabaseManager:
    def __init__(self, testing=False):
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
            self.con = sqlite3.connect(path)
            self.cur = self.con.cursor()

            # Build the tables if they don't exist
            self.set_up_users_table()
            self.set_up_categories_table()
            self.set_up_payment_methods_table()
            self.set_up_expenses_table()

            # Commit pending transactions to the database then close the connection
            self.con.commit()
 
            print("Database", name, " has been connected")

        except sqlite3.Error as e:
            print(e)

    def close_connection(self):
        """
        Close the database's connection if it is open
        """
        self.con.close()

    def set_up_users_table(self):
        """
        Create the table for the users
        """
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT,
                        created_at DATETIME,
                        updated_at DATETIME
                    )
                    """)
        self.con.commit()

    def set_up_categories_table(self):
        """
        Create the table for the categories
        """
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS categories(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT UNIQUE NOT NULL,
                        created_at DATETIME,
                        updated_at DATETIME,
                    
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                    """)
        self.con.commit()
        
        
        # Inserting default categories
        for category in DEFAULT_CATEGOREIS:
            add_category(None, category, self)

    def set_up_payment_methods_table(self):
        """
        Create the table for the payment methods
        """
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS payment_methods(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT UNIQUE NOT NULL,
                        created_at DATETIME,
                        updated_at DATETIME,
                    
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                    """)
        self.con.commit()
        
        # Inserting default payment methods
        for payment_method in DEFAULT_PAYMENT_METHODS:
            add_payment_method(None, payment_method, self)

    def set_up_expenses_table(self):
        """
        Create the table for the expenses
        """
        self.cur.execute("""
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
        self.con.commit()

    def clear_tables(self):
        """
        Empty the tables in the database
        """
        self.cur.execute("DELETE FROM expenses")
        self.cur.execute("DELETE FROM categories")
        self.cur.execute("DELETE FROM payment_methods")
        self.cur.execute("DELETE FROM users")
        self.con.commit()

        # Leave the defaults alone
        for payment_method in DEFAULT_PAYMENT_METHODS:
            add_payment_method(None, payment_method, self)
        for category in DEFAULT_CATEGOREIS:
            add_category(None, category, self)
    
    def execute_statement(self, sql, val):
        """
        Executes a SQL query made by other files

        Arugments:
            sql (string): The SQL statement to be executed
            val (tuple): Tuple of values to replace placeholders in the statement
        """
        try:
            self.cur.execute(sql, val)
            self.con.commit()

            return True
        
        except Exception as e:
            print(e)
            return False