# Author - Daniel Dang
# Filename - forecast.py
# Purpose - Provides functionality for performing a time series analysis for detecting trends and anomalies

import pandas as pd
import numpy as np
import datetime
import copy
import math
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

    # plt.scatter(x_train, y_train, marker='x')
    # plt.title("Spending per Day")
    # plt.ylabel("Spending Amount")
    # plt.xlabel("Day Number")
    # plt.show()

    # initial_w = 0
    # initial_b = 0
    # cost = compute_cost(x_train, y_train, initial_w, initial_b)
    # print(cost)

    # tmp_dw, tmp_db = compute_gradient(x_train, y_train, initial_w, initial_b)
    # print("d_dw: " + str(tmp_dw))
    # print("d_db: " + str(tmp_db))

    initial_w = 0.
    initial_b = 0.
    alpha = 0.01
    num_iters = 1000
    x_normalized = z_score_normalization(x_train)
    y_normalized = z_score_normalization(y_train)
    w, b, j_history, w_history = graient_descent(x_normalized, y_normalized, initial_w, initial_b, alpha, num_iters)
    print()
    print("Gradient Descent Results")
    print("w: " + str(w))
    print("b: " + str(b))

    plot_linear_regression(x_normalized, y_normalized, w, b)

    print("Predicted Spending: " + str())

    

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

    total_cost = cost / (2*m)

    return total_cost

def compute_gradient(x, y, w, b):
    """
    Compute the gradient for linear regression

    Arguments:
        x (np.ndarray): Data for x-axes (day numbers)
        y (np.ndarray): Data for y-axes (spending amount)
        w, b (float): Parameters of the model

    Returns:
        d_dw (float): Rate of change for w
        d_db (float): Rate of change for b
    """
    # Length of training data
    m = x.shape[0]

    d_dw = 0
    d_db = 0

    # Calculate rates of change for w and b 
    for i in range(m):
        f_wb = (w * x[i]) + b

        d_dw += (f_wb - y[i]) * x[i]
        d_db += (f_wb - y[i])

    d_dw /= m
    d_db /= m

    return d_dw, d_db

def z_score_normalization(data):
    """
    Normalize data using the z-score normalization method

    Argument:
        data (np.ndarray): Data to normalize
    """
    avg = np.mean(data)
    std = np.std(data)

    if std == 0:
        std = 1

    data_normalized = (data - avg) / std
    return data_normalized

def graient_descent(x, y, w_input, b_input, alpha, num_iters):
    """
    Perform gradient descent to find local minimum

    Arguments:
        x (np.ndarray): Data for x-axes (day numbers)
        y (np.ndarray): Data for y-axes (spending amount)
        w_input, b_input (float): Parameters of the model
        alpha (float): Learning rate
        num_iters (int): Number of iterations
    """
    # Keep track of cost function and w values at each iteration for graphing
    j_history = []
    w_history = []

    w = copy.deepcopy(w_input)
    b = (b_input)

    for i in range(num_iters):
        d_dw, d_db = compute_gradient(x, y, w, b)
        
        tmp_w = w - (alpha * d_dw)
        w = tmp_w
        tmp_b = b - (alpha * d_db)
        b = tmp_b

        if i < 100000:
            cost_function = compute_cost(x, y, w, b)
            j_history.append(cost_function)

        # Print cost function every 100 iterations
        if i% math.ceil(num_iters/10) == 0:
            w_history.append(w)
            print(f"Iteration {i:4}: Cost {float(j_history[-1]):8.2f}   ")

    return w, b, j_history, w_history

def plot_linear_regression(x,y, w, b):
    """
    Plot linear regression

    Arguments:
        x (np.ndarray): Data for x-axes (day numbers)
        y (np.ndarray): Data for y-axes (spending amount)
        w, b (float): Parameters of the model
    """

    # Length of training data
    m = x.shape[0]
    predicted = np.zeros(m)

    for i in range(m):
        predicted[i] = w * x[i] + b

    plt.plot(x, predicted)
    plt.scatter(x, y, marker='x', c='r')
    plt.title("Spending per Day")
    plt.ylabel("Spending Amount")
    plt.xlabel("Day Number")
    plt.show()