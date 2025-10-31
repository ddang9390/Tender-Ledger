# Author - Daniel Dang
# Filename - expenses.py
# Purpose - Handles adding, updating, and deleting expenses

from datetime import datetime

def add_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, db):
    """
    Add an expense for the user

    Arguments:
        user_id (int): The user's id
        amount (float): Amount of the purchase
        date_of_purchase (string): Date when purchase was made
        payment_method_id (int): Payment method used for expense
        category_id (int): Expense's category
        location (string): Other details about the expense
        db (DatabaseManager): Instance of database manager being used

    Returns:
        bool: True if able to add expense
              False if not
    """
    created_at = datetime.now()
    sql = "INSERT INTO expenses (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    val = (user_id, amount, date_of_purchase, payment_method_id, category_id, location, created_at)

    return db.execute_statement(sql, val)

def update_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, testing=False):
    """
    Update an expense for the user

    Arguments:
        user_id (int): The user's id
        amount (float): Amount of the purchase
        date_of_purchase (string): Date when purchase was made
        payment_method_id (int): Payment method used for expense
        category_id (int): Expense's category
        location (string): Other details about the expense
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB

    Returns:
        bool: True if able to update expense
              False if not
    """
    updated_at = datetime.now()

def delete_expense(id, testing=False):
    """
    Delete an expense for the 

    Arguments:
        id (int): ID of the expense
        testing (bool): If True, the testing DB will be used
                        Else, use the prod DB

    Returns:
        bool: True if able to delete expense
              False if not
    """
    pass

def get_expenses_for_user(user_id, db, start_date=None, end_date=None, category=None, payment_method=None, search=None, order=None):
    """
    Gets all expenses for a user

    Arguments:
        user_id (int): Id of the user
        db (DatabaseManager): Instance of database manager being used
        start_date (string): Start date for searching
        end_date (string): End date for searching
        category (int): Category being searched for
        payment_method (int): Payment method being searched for
        search (string): Term being searched for from search bar
        order: Column being sorted

    Returns:
        list: List of the user's expenses
    """
    select_clause = """
                    SELECT
                        e.amount,
                        e.date_of_purchase,
                        p.name AS payment_method_name,
                        c.name AS category_name,
                        e.location
                    FROM
                        expenses e
                    LEFT JOIN
                        categories c ON e.category_id = c.id
                    LEFT JOIN
                        payment_methods p ON e.payment_method_id = p.id
                    """
    where_clause = """
                    WHERE
                        e.user_id = ?
                   """
    order_by_clause = """
                      ORDER BY
                        e.date_of_purchase DESC
                      """
    val = [user_id,]

    # Handling filtering
    if start_date:
        where_clause += ("AND e.date_of_purchase >= ?")
        val.append(start_date)
    
    if end_date:
        where_clause += (" AND e.date_of_purchase <= ?")
        val.append(end_date)

    if category:
        where_clause += (" AND e.category_id = ?")
        val.append(category)

    if payment_method:
        where_clause += (" AND e.payment_method_id = ?")
        val.append(payment_method)

    if search:
        where_clause += (" AND (e.amount LIKE ? OR e.location LIKE ?)")
        val.extend([f"%{search}%", f"%{search}%"])

    # Handling sorting by columns
    if order:
        pass

    sql = select_clause + where_clause + order_by_clause


    try:
        db.cur.execute(sql, val)
        return db.cur.fetchall()
    except Exception as e:
        print(e)
        return []