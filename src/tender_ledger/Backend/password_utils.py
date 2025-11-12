# Author - Daniel Dang
# Filename - password_utils.py
# Purpose - Provide functions for hashing and verifying passwords

import bcrypt

def hash_password(pw):
    """
    Hash the password for better security

    Arguments:
        pw (str): User input for the password

    Returns:
        hashed_pw (str): The password after being hashed
    """
    # Convert password to bytes
    pw_bytes = pw.encode('utf-8')

    # Generate salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_pw= bcrypt.hashpw(password=pw_bytes, salt=salt)
    return hashed_pw

def verify_password(pw, hashed_pw):
    """
    Verifies that the password matches

    Arguments:
        pw (str): User input for the password
        hashed_pw (str): Password gotten from the database

    Returns:
        bool: True if matches
              False if not
    """
    pw_bytes = pw.encode('utf-8')
    return bcrypt.checkpw(pw_bytes, hashed_pw)