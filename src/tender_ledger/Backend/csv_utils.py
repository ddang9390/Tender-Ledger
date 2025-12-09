# Author - Daniel Dang
# Filename - csv_utils.py
# Purpose - Handles downloading and importing csv files

import pandas as pd
from tkinter import filedialog
from .categories import get_categories_for_user, add_category, get_category_by_name
from .payment_methods import get_payment_methods_for_user, add_payment_method, get_payment_method_by_name
from .expenses import add_expense


COLUMN_NAMES = ['Date', 'Amount', 'Category', 'Payment Method', 'Location']

def download_expenses_csv(expenses):
    """
    Download a csv file using a list of expenses

    Argument:
        expenses (list): List of tuples that represent the expenses
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save File As"
    )
    if file_path:
        df = pd.DataFrame(expenses, columns= COLUMN_NAMES)
        df.to_csv(file_path, index=False)

def open_file(user_id, db):
    """
    Opens a file dialog asking the user to open a csv file.
    If the file path is valid, import the contents as the user's expenses

    Arguments:
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used
    """
    file_path = filedialog.askopenfilename(
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")],
        title="Select Expenses CSV"
    )

    if file_path:
        return import_expenses_csv(file_path, user_id, db)
    
    return False

def import_expenses_csv(file_path, user_id, db):
    """
    Import expenses from a csv file

    Arguments:
        file_path (string): Path to the file
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used
    """
    try:
        categories = list(get_categories_for_user(user_id, db).keys())
        payment_methods = list(get_payment_methods_for_user(user_id, db).keys())
        df = pd.read_csv(file_path)

        for i, row in df.iterrows():
            date = row['Date']
            amount = row['Amount']
            category = row['Category']
            payment_method = row['Payment Method']
            location = row['Location']

            # Formatting date
            try:
                date_obj = pd.to_datetime(date)
                date = date_obj.strftime('%Y-%m-%d')
            except:
                print(f"Skipping row {i}: Invalid date format {date}")
                continue

            # Check if category and payment method already exists
            if category not in categories:
                add_category(user_id, category, db)

            if payment_method not in payment_methods:
                add_payment_method(user_id, payment_method, db)

            category_id = get_category_by_name(category, db)[0][0]
            payment_method_id = get_payment_method_by_name(payment_method, db)[0][0]

            # Skip duplicates
            if check_duplicate(user_id, db, date, amount, category_id, payment_method_id, location):
                continue

            add_expense(user_id, amount, date, payment_method_id, category_id, location, db)
            
        return True

    except Exception as e:
        print(e)
        return False
    
def check_duplicate(user_id, db, date_of_purchase, amount, category_id, payment_method_id, location):
    """
    Check if the expense already exists for the user

    Aruguments:
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used
        date_of_purchase (string): Date when purchase was made
        amount (float): Amount of the purchase
        category_id (int): Expense's category
        payment_method_id (int): Payment method used for expense
        location (string): Other details about the expense

    Returns:
        bool: True if the expense exists
              False if not or if was unable to access the database
    """
    try:
        sql = """
              SELECT *
              FROM expenses
              WHERE
                user_id = ? AND
                date_of_purchase = ? AND
                amount = ? AND
                category_id = ? AND
                payment_method_id = ? AND
                location = ?
              """
        
        vals = (user_id, date_of_purchase, amount, category_id, payment_method_id, location)
        db.cur.execute(sql, vals)
        expense = db.cur.fetchone()

        return expense is not None

    except Exception as e:
        print(e)
        return False