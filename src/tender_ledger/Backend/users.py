# Author - Daniel Dang
# Filename - users.py
# Purpose - Handles adding, updating, and deleting users

from datetime import datetime

def add_user(username, password, cur, con):
    """
    Add a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """
    created_at = datetime.now()

    sql = "INSERT INTO categories (username, password, created_at) VALUES (?, ?, ?)"
    val = (username, password, created_at)

    # Execute the query then commit the changes
    try:
        cur.execute(sql, val)
        con.commit()
    except Exception as e:
        print(e)

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