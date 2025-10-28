# Author - Daniel Dang
# Filename - users.py
# Purpose - Handles adding, updating, and deleting users

from datetime import datetime

def add_user(username, password, testing=False):
    """
    Add a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    created_at = datetime.now()

def update_user(username, password, testing=False):
    """
    Update a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    updated_at = datetime.now()

def delete_user(id, testing=False):
    """
    Delete a user

    Arguments:
        id (int): The user's id
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB
    """
    pass