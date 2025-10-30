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

    Returns:
        bool: True if able to add user
              False if not
    """
    created_at = datetime.now()

    sql = "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?);"
    val = (username, password, created_at)

    # Execute the query then commit the changes
    try:
        cur.execute(sql, val)
        con.commit()
        return True
    
    except Exception as e:
        print(e)
        return False

def update_user(username, password, cur, con):
    """
    Update a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database

    Returns:
        bool: True if able to update user
              False if not
    """
    updated_at = datetime.now()

def delete_user(username, cur, con):
    """
    Delete a user

    Arguments:
        username (string): The user's username
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database

    Returns:
        bool: True if able to delete user
              False if not
    """
    sql = "DELETE FROM users WHERE username = '" + username + "'"

    try:
        cur.execute(sql)
        con.commit()

        return True
    
    except Exception as e:
        print(e)
        return False