# Author - Daniel Dang
# Filename - users.py
# Purpose - Handles adding, updating, and deleting users

from datetime import datetime

def add_user(username, password, db):
    """
    Add a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add user
              False if not
    """
    created_at = datetime.now()

    sql = "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?);"
    val = (username, password, created_at)

    return db.execute_statement(sql, val)

def update_user(username, password, db):
    """
    Update a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to update user
              False if not
    """
    updated_at = datetime.now()

def delete_user(username, db):
    """
    Delete a user

    Arguments:
        username (string): The user's username
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to delete user
              False if not
    """
    sql = "DELETE FROM users WHERE username = ?"
    val = (username,)

    return db.execute_statement(sql, val)
