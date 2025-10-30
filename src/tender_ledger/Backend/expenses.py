# Author - Daniel Dang
# Filename - expenses.py
# Purpose - Handles adding, updating, and deleting expenses

from datetime import datetime

def add_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, db):
    """
    Add an expense for the user

    Arguments:
        user_id (int): The user's id
        amount (float): Amount of the purchase
        date_of_purchase (string): Date when purchase was made
        payment_method_id (int): Payment method used for expense
        category_id (int): Expense's category
        location (string): Other details about the expense
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add expense
              False if not
    """
    created_at = datetime.now()
    sql = "INSERT INTO expenses (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    val = (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at)

    return db.execute_statement(sql, val)

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

    Returns:
        bool: True if able to update expense
              False if not
    """
    updated_at = datetime.now()

def delete_expense(id, testing=False):
    """
    Delete an expense for the 

    Arguments:
        id (int): ID of the expense
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB

    Returns:
        bool: True if able to delete expense
              False if not
    """
    pass

def get_expenses_for_user(user_id, db):
    """
    Gets all expenses for a user

    Arguments:
        user_id (int): Id of the user
        db (DatabaseManager): Instance of database manager being used

    Returns:
        list: List of the user's expenses
    """
    sql = """
            SELECT
                e.amount,
                e.date_of_purchase,
                p.name AS payment_method_name,
                c.name AS category_name,
                e.location
            FROM
                expenses e
            LEFT JOIN
                categories c ON e.category_id = c.id
            LEFT JOIN
                payment_methods p ON e.payment_method_id = p.id
            WHERE
                e.user_id = ?
          """
    val = (user_id,)

    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)
        return []