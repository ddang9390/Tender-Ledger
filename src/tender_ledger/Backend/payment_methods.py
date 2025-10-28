# Author - Daniel Dang
# Filename - payment_methods.py
# Purpose - Handles adding, updating, and deleting custom payment methods

from datetime import datetime

def add_payment_method(user_id, name, testing=False):
    """
    Add a custom payment method for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom payment method's name
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    created_at = datetime.now()

def update_payment_method(user_id, name, testing=False):
    """
    Update a custom payment method for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom payment method's name
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    updated_at = datetime.now()

def delete_payment_method(id, testing=False):
    """
    Delete a custom payment method for the user

    Arguments:
        id (int): The custom payment method's id
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    pass