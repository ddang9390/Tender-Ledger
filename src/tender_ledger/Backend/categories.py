# Author - Daniel Dang
# Filename - categories.py
# Purpose - Handles adding, updating, and deleting custom categories

from datetime import datetime

def add_category(user_id, name, testing=False):
    """
    Add a custom category for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom category's name
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    created_at = datetime.now()

def update_category(user_id, name, testing=False):
    """
    Update a custom category for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom category's name
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    updated_at = datetime.now()

def delete_category(id, testing=False):
    """
    Delete a custom category for the user

    Arguments:
        id (int): The custom category's id
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    pass