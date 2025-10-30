# Author - Daniel Dang
# Filename - categories.py
# Purpose - Handles adding, updating, and deleting custom categories

from datetime import datetime

def add_category(user_id, name, cur, con):
    """
    Add a custom category for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom category's name
        cur (Cursor): Cursor instance that is used to execute SQL statements
        con (Connection): Connection to the database
    """

    created_at = datetime.now()

    sql = "INSERT INTO categories (user_id, name, created_at) VALUES (?, ?, ?)"
    val = (user_id, name, created_at)

    # Execute the query then commit the changes
    try:
        cur.execute(sql, val)
        con.commit()
    except Exception as e:
        print(e)


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