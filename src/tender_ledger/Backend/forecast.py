# Author - Daniel Dang
# Filename - forecast.py
# Purpose - Provides functionality for performing a time series analysis for detecting trends and anomalies

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression 

# TODO - break forecast file into separate files for feature creation and linear regression
def forecast(expenses):
    df = create_dataframe(expenses)
    daily_spending = get_daily_spending(df)

    x_train, y_train = create_features(daily_spending)

    
    print(x_train.shape)
    print(y_train.shape)
    print()

    print(type(x_train))
    print(x_train[:5])

    print(type(y_train))
    print(y_train[:5])

    plt.scatter(x_train, y_train, marker='x')
    plt.title("Spending per Day")
    plt.ylabel("Spending Amount")
    plt.xlabel("Day Number")
    plt.show()

    initial_w = 2
    initial_b = 1
    cost = compute_cost(x_train, y_train, initial_w, initial_b)
    print(cost)

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
    
    # Remove unnecessary columns and reorder the dataframe
    df = df[['Date', 'Amount', 'Category', 'Payment Method']]

    # Convert strings to dates
    df['Date'] = pd.to_datetime(df['Date'])

    df = df.sort_values('Date').reset_index(drop=True)

    return df

def get_daily_spending(df):
    """
    Get daily spending using expenses dataframe

    Argument:
        df (pd.DataFrame): Expenses converted to a cleaned Pandas DataFrame

    Returns:
        daily_spending (pd.DataFrame): Dataframe containing the total amount spent per day 
    """
    daily_spending = df.groupby('Date')['Amount'].sum().sort_index()
    
    # Fill in missing dates with 0 spending
    full_date_range = pd.date_range(start=daily_spending.index.min(), 
                                     end=daily_spending.index.max(), 
                                     freq='D')
    daily_spending = daily_spending.reindex(full_date_range, fill_value=0)
    
    return daily_spending


def create_features(df):
    """
    Create features for linear regression to predict future spending

    Argument:
        df (pd.DataFrame): Expenses converted to a cleaned Pandas DataFrame

    Returns:
        x_train (np.ndarray): feature for the days
        y_train (np.ndarray): feature for the spending per day
    """
    m = len(df)

    x_train = np.arange(m).reshape(-1, 1)
    y_train = df.values

    return x_train, y_train

def compute_cost(x, y, w, b):
    """
    Compute the cost function for linear regression

    Arguments:
        x (np.ndarray): Data for x-axes (day numbers)
        y (np.ndarray): Data for y-axes (spending amount)
        w, b (float): Parameters of the model

    Returns:
        cost (float): Cost of using the model for linear regression
    """
    # Length of training data
    m = x.shape[0]

    # Compute cost function
    cost = 0
    for i in range(m):
        f_wb = (w * x[i]) + b
        cost += (f_wb - y[i])**2

    cost /= (2*m)

    return cost