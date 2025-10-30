# Author - Daniel Dang
# Filename - payment_methods.py
# Purpose - Handles adding, updating, and deleting custom payment methods

from datetime import datetime

def add_payment_method(user_id, name, db):
    """
    Add a custom payment method for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom payment method's name
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add payment method
              False if not
    """

    created_at = datetime.now()

    sql = "INSERT INTO payment_methods (user_id, name, created_at) VALUES (?, ?, ?)"
    val = (user_id, name, created_at)

    return db.execute_statement(sql, val)

def update_payment_method(user_id, name, testing=False):
    """
    Update a custom payment method for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom payment method's name
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB

    Returns:
        bool: True if able to update payment method
              False if not
    """
    updated_at = datetime.now()

def delete_payment_method(id, testing=False):
    """
    Delete a custom payment method for the user

    Arguments:
        id (int): The custom payment method's id
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB

    Returns:
        bool: True if able to delete payment method
              False if not
    """
    pass