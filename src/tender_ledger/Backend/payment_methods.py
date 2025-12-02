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

def update_payment_method(id, name, db):
    """
    Update a custom payment method for the user

    Arguments:
        id (int): The payment method's id
        name (string): The custom payment method's name
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to update payment method
              False if not
    """
    updated_at = datetime.now()

    sql = """
          UPDATE payment_methods
          SET
            name = ?,
            updated_at = ?
          WHERE id = ?
          """
    val = (name, updated_at, id,)
    return db.execute_statement(sql, val)

def delete_payment_method(id, db):
    """
    Delete a custom payment method for the user

    Arguments:
        id (int): The custom payment method's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to delete payment method
              False if not
    """
    sql = """
            DELETE FROM payment_methods
            WHERE id = ?
          """
    val = (id,)

    return db.execute_statement(sql, val)

def get_payment_methods_for_user(user_id, db):
    """
    Gets the custom payment methods made by the user along with
    the default methods

    Arguments:
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        dict: A dictionary containing the payment method's name as the key
              and the payment method's id as the value
    """
    payment_methods = {}
    try:
        sql = """
                SELECT id, name 
                FROM payment_methods
                WHERE user_id = ? OR user_id IS NULL
              """
        
        db.cur.execute(sql, (user_id,))
        rows = db.cur.fetchall()

        for row in rows:
            payment_methods[row[1]] = row[0]
        
        return payment_methods

    except Exception as e:
        print("fsdfd")
        print(e)
        return payment_methods
    
def get_payment_methods_for_list(user_id, db):
    """
    Gets the payment methods for the Customizations tab from the Profile page

    Arguments:
        user_id (int): The user's id
        db (DatabaseManager): Instance of database manager being used

    Returns:
        list: A list containing the method's id, name, and corresponding user id
    """
    try:
        sql = """
                SELECT id, name, user_id
                FROM payment_methods
                WHERE user_id = ? OR user_id IS NULL
              """
        
        db.cur.execute(sql, (user_id,))
        rows = db.cur.fetchall()
        
        return rows

    except Exception as e:
        print(e)
        return []
    
    
def get_payment_method(id, db):
    """
    Get a single payment method

    Arguments:
        id (int): ID of the payment method
        db (DatabaseManager): Instance of database manager being used

    Returns:
        list: Contains a tuple that contains info about the payment method
    """
    select_clause = """
                    SELECT
                        id, name, user_id
                    FROM
                        payment_methods
                    """
    where_clause = """
                    WHERE
                        id = ?
                   """
    val = [id,]

    sql = select_clause + where_clause
    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)
        return []
    
def get_payment_method_by_name(name, db):
    """
    Get a single payment method

    Arguments:
        name (string): Name of the payment method
        db (DatabaseManager): Instance of database manager being used

    Returns:
        list: Contains a tuple that contains info about the payment method
    """
    select_clause = """
                    SELECT
                        id, name, user_id
                    FROM
                        payment_methods
                    """
    where_clause = """
                    WHERE
                        name = ?
                   """
    val = [name,]

    sql = select_clause + where_clause
    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)
        return []