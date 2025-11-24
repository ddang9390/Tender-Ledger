# Author - Daniel Dang
# Filename - csv_utils.py
# Purpose - Handles downloading and importing csv files

import pandas as pd

COLUMN_NAMES = ['Date', 'Amount', 'Category', 'Payment Method', 'Location']

def download_expenses_csv(expenses):
    """
    Download a csv file using a list of expenses

    Argument:
        expenses (list): List of tuples that represent the expenses
    """
    df = pd.DataFrame(expenses, columns= COLUMN_NAMES)
    df.to_csv('output.csv', index=False)

def import_expenses_csv(file):
    print(file)
    # NOTE - csv files may contain categories and payment methods that weren't in the table