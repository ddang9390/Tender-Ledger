# Author - Daniel Dang
# Filename - path_utils.py
# Purpose - Utilities for handling paths

import sys
from pathlib import Path

# Database names
DB_NAME = 'tender_ledger.db'
TEST_DB_NAME = 'test_tender_ledger.db'

# JSON files for custom themes
THEME_NAME = 'GUI/theme.json'

def get_base_path():
    """
    Get the base path for the application.
    
    Returns:
        Path: The base directory path
    """
    # If program is ran as an executable
    if getattr(sys, 'frozen', False):
        # If there are bundled files like a theme.json file
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS)
        else:
            return Path(sys.executable).parent
    
    # Else it is a normal process
    else:
        return Path(__file__).parent.parent


def get_data_dir():
    """
    Get the directory where the database should be stored.
    
    Returns:
        Path: The data directory path
    """
    # If program is ran as an executable
    if getattr(sys, 'frozen', False):
        # Store data next to exe file
        base = Path(sys.executable).parent
    else:
        # Using root folder
        base = Path(__file__).parent.parent
    
    data_dir = base / 'data'
    data_dir.mkdir(exist_ok=True)
    
    return data_dir


def get_database_path(testing):
    """
    Get the full path to the database file.

    Argument:
        testing (bool): True if we want the test database
                        False if we want the database for the prod environment
    
    Returns:
        Path: Full path to database
    """
    if not testing:
        return get_data_dir() / DB_NAME
    else:
        return get_data_dir() / TEST_DB_NAME


def get_theme_path():
    """
    Get the full path to the theme file
    
    Returns:
        Path: Full path to theme file
    """
    return get_base_path() / THEME_NAME