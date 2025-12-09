# Author - Daniel Dang
# Filename - forecast.py
# Purpose - Provides functionality for performing a time series analysis for detecting trends and anomalies

import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression 


def forecast(expenses):
    df = create_dataframe(expenses)
    daily_spending = get_daily_spending(df)

    print(daily_spending)

def create_dataframe(expenses):
    """
    Create dataframe from expenses for analysis
    
    Argument: 
        expenses (list): List of expenses

    Returns:
        df (pd.DataFrame): Expenses converted to a cleaned Pandas DataFrame  
    """
    columns = ['Amount', 'Date', 'Payment Method', 'Category', 'Location', 'id']

    df = pd.DataFrame(expenses, columns=columns)
    df = df[['Date', 'Amount', 'Category', 'Payment Method']]

    # Convert strings to dates
    df['Date'] = pd.to_datetime(df['Date'])

    return df

def get_daily_spending(df):
    """
    Get daily spending using expenses dataframe

    Argument:
        df (pd.DataFrame): Expenses converted to a cleaned Pandas DataFrame

    Returns:
        daily_spending (pd.DataFrame): Dataframe containing the total amount spent per day 
    """
    daily_spending = df.groupby('Date')['Amount'].sum()
    return daily_spending