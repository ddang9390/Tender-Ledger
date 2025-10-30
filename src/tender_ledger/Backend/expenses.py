# Author - Daniel Dang
# Filename - expenses.py
# Purpose - Handles adding, updating, and deleting expenses

from datetime import datetime

def add_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, cur, con):
    """
    Add an expense for the user

    Arguments:
        user_id (int): The user's id
        amount (float): Amount of the purchase
        date_of_purchase (string): Date when purchase was made
        payment_method_id (int): Payment method used for expense
        category_id (int): Expense's category
        location (string): Other details about the expense
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """
    created_at = datetime.now()
    sql = "INSERT INTO expenses (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    val = (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at)

    # Execute the query then commit the changes
    try:
        cur.execute(sql, val)
        con.commit()
    except Exception as e:
        print(e)

def update_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, testing=False):
    """
    Update an expense for the user

    Arguments:
        user_id (int): The user's id
        amount (float): Amount of the purchase
        date_of_purchase (string): Date when purchase was made
        payment_method_id (int): Payment method used for expense
        category_id (int): Expense's category
        location (string): Other details about the expense
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    updated_at = datetime.now()

def delete_expense(id, testing=False):
    """
    Delete an expense for the 

    Arguments:
        id (int): ID of the expense
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    pass