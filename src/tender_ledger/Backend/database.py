# Author - Daniel Dang
# Filename - database.py
# Purpose - To setup the database for the Tender Ledger project

import sqlite3
from .categories import add_category
from .payment_methods import add_payment_method
from .path_utils import get_database_path

# Names of databases
DB_NAME = "tender_ledger.db"
TEST_DB_NAME = "test_tender_ledger.db"

DEFAULT_CATEGORIES = ["Food", 
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
        name = TEST_DB_NAME if testing else DB_NAME
        path = get_database_path(testing)

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
 
            print("Database", name, "has been connected")

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
                        password TEXT NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        birthday DATETIME,
                        email TEXT UNIQUE NOT NULL,
                        phone INTEGER NOT NULL,
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
                        name TEXT NOT NULL,
                        created_at DATETIME,
                        updated_at DATETIME,
                    
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        
                        UNIQUE(user_id, name)
                    )
                    """)
        self.con.commit()
        
        
        # Inserting default categories
        self.insert_default_categories()

    def set_up_payment_methods_table(self):
        """
        Create the table for the payment methods
        """
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS payment_methods(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT NOT NULL,
                        created_at DATETIME,
                        updated_at DATETIME,
                    
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                         
                        UNIQUE(user_id, name)
                    )
                    """)
        self.con.commit()
        
        # Inserting default payment methods
        self.insert_default_payment_methods()

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
                    
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id) ON DELETE SET NULL,
                        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
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
        self.insert_default_payment_methods()
        self.insert_default_categories()
    
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
        
    def insert_default_payment_methods(self):
        """
        Insert default payment methods if they don't already exist
        """
        for payment_method in DEFAULT_PAYMENT_METHODS:
            self.cur.execute("SELECT id FROM payment_methods WHERE name = ? AND user_id IS NULL", (payment_method,))
            if self.cur.fetchone() is None:
                add_payment_method(None, payment_method, self)

    def insert_default_categories(self):
        """
        Insert default categories if they don't already exist
        """
        for category in DEFAULT_CATEGORIES:
            self.cur.execute("SELECT id FROM categories WHERE name = ? AND user_id IS NULL", (category,))
            if self.cur.fetchone() is None:
                add_category(None, category, self)