# Author - Daniel Dang
# Filename - users.py
# Purpose - Handles adding, updating, and deleting users

from datetime import datetime

def add_user(username, password, first_name, last_name, birthday, email, phone, db):
    """
    Add a user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        first_name (string): The user's first name
        last_name (string): The user's last name
        birthday (string): The user's birthday
        email (string): The user's email
        phone (int): The user's phone number
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add user
              False if not
    """
    created_at = datetime.now()

    sql = "INSERT INTO users (username, password, first_name, last_name, birthday, email, phone, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    val = (username, password, first_name, last_name, birthday, email, phone, created_at)

    return db.execute_statement(sql, val)

def update_user(id, username, password, first_name, last_name, birthday, email, phone, db):
    """
    Update a user

    Arguments:
        id (int): The user's id
        username (string): The user's username
        password (string): The user's password
        first_name (string): The user's first name
        last_name (string): The user's last name
        birthday (string): The user's birthday
        email (string): The user's email
        phone (int): The user's phone number
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to update user
              False if not
    """
    updated_at = datetime.now()
    sql = """
            UPDATE users
            SET 
                username = ?,
                password = ?,
                first_name = ?,
                last_name = ?,
                birthday = ?,
                email = ?,
                phone = ?,
                updated_at = ?
            WHERE
                id = ?
          """
    
    val = (username, password, first_name, last_name, birthday, email, phone, updated_at, id)

    return db.execute_statement(sql, val)
    

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

def get_user(username, password, db):
    """
    Finds a matching user

    Arguments:
        username (string): The user's username
        password (string): The user's password
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to get user
              False if not
    """
    sql = """
          SELECT *
          FROM users
          WHERE
            username = ?
            AND password = ?
          """
    val = (username, password,)

    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)

def get_user_by_username(username, db):
    """
    Finds a matching user by just their username

    Arguments:
        username (string): The user's username
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to get user
              False if not
    """
    sql = """
          SELECT *
          FROM users
          WHERE
            username = ?
          """
    val = (username,)

    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)

def get_user_by_id(id, db):
    """
    Finds a matching user by just their id

    Arguments:
        id (int): The user's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to get user
              False if not
    """
    sql = """
          SELECT *
          FROM users
          WHERE
            id = ?
          """
    val = (id,)

    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)

def check_if_username_exists(id, username, db):
    """
    Checks if a username already exists and is not being used
    by the current user

    Arguments:
    """
    sql = """
            SELECT
                COUNT(*)
            FROM users
            WHERE 
                id != ? AND
                username = ?
          """
    val = [id, username]
    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()[0][0] != 0
    except Exception as e:
        print(e)