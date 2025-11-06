# Author - Daniel Dang
# Filename - categories.py
# Purpose - Handles adding, updating, and deleting custom categories

from datetime import datetime

def add_category(user_id, name, db):
    """
    Add a custom category for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom category's name
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add category
              False if not
    """

    created_at = datetime.now()

    sql = "INSERT INTO categories (user_id, name, created_at) VALUES (?, ?, ?)"
    val = (user_id, name, created_at)

    return db.execute_statement(sql, val)
    


def update_category(user_id, name, db):
    """
    Update a custom category for the user

    Arguments:
        user_id (int): The user's id
        name (string): The custom category's name
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to update category
              False if not
    """
    updated_at = datetime.now()

def delete_category(id, db):
    """
    Delete a custom category for the user

    Arguments:
        id (int): The custom category's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to delete category
              False if not
    """
    pass

def get_categories_for_user(user_id, db):
    """
    Gets the custom categories made by the user along with
    the default categories

    Arguments:
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        dict: A dictionary containing the category's name as the key
              and the category's id as the value
    """
    categories = {}
    try:
        sql = """
                SELECT id, name 
                FROM categories
                WHERE user_id = ? OR user_id IS NULL
              """
        
        db.cur.execute(sql, (user_id,))
        rows = db.cur.fetchall()

        for row in rows:
            categories[row[1]] = row[0]
        
        return categories

    except Exception as e:
        print(e)
        return categories