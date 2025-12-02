# Author - Daniel Dang
# Filename - dashboard.py
# Purpose - Generates the charts for the dashboard

import datetime
import numpy as np
from matplotlib.figure import Figure


# Defining constants which are the indices of the elements that
# appear in the expenses list
CATEGORY_INDEX = 3
PAYMENT_METHOD_INDEX = 2
AMOUNT_INDEX = 0

def generate_pie_charts(expenses):
    """
    Generates a pie chart for the dashboard page that shows
    how the expenses are distributed by category and payment method

    Argument:
        expenses (List): List of the user's expenses

    Returns:
        category_pie: Pie chart representing distribution by categories
        payment_method_pie: Pie chart representing distribution by payment methods
    """
    categories = {}
    payment_methods = {}

    for expense in expenses:
        category = expense[CATEGORY_INDEX]
        # Gathering categories that expenses used
        if category not in categories.keys():
            categories[category] = 0

        # Gathering payment methods that expenses used
        payment_method = expense[PAYMENT_METHOD_INDEX]
        if payment_method not in payment_methods.keys():
            payment_methods[payment_method] = 0

        # Sum up number of times categories and payment methods were used
        categories[category] += 1
        payment_methods[payment_method] += 1

    # Making pie chart for distribution by categories
    category_pie = Figure()
    category_pie_axes = category_pie.add_subplot(111)
    category_pie_axes.pie(categories.values(), labels = categories.keys(), autopct='%1.1f%%')
    category_pie_axes.set_title('Distribution by Categories')

    # Making pie chart for distribution by payment methods
    payment_method_pie = Figure()
    payment_method_pie_axes = payment_method_pie.add_subplot(111)
    payment_method_pie_axes.pie(payment_methods.values(), labels = payment_methods.keys(), autopct='%1.1f%%')
    payment_method_pie_axes.set_title('Distribution by Payment Methods')
    
    return category_pie, payment_method_pie

def generate_line_plot(expenses):
    """
    Generates a line plot showing how spending is distributed in a date range

    Argument:
        expenses (List): List of the user's expenses

    Returns:
        line_plot: Line plot representing spending distribution
    """
    spending = {}
    # Gather expenses and track amount of spending per day
    for expense in expenses:
        date = datetime.datetime.strptime(expense[1], "%Y-%m-%d").date()
        if date in spending.keys():
            spending[date] += expense[0]
        else:
            spending[date] = expense[0]

    sorted_spending = dict(sorted(spending.items()))

    # Make line plot
    line_plot = Figure()
    line_plot_axes = line_plot.add_subplot(111)

    line_plot_axes.plot(sorted_spending.keys(), sorted_spending.values(), marker='o')
    line_plot_axes.set_title("Daily Spending")
    line_plot_axes.set_xlabel("Dates")
    line_plot_axes.set_ylabel("Amount")
    line_plot_axes.tick_params(axis='x', labelrotation=45)

    return line_plot

def generate_bar_chart(expenses):
    """
    Generates a horizontal bar chart showing the ranking of categories by total spending

    Argument:
        expenses (List): List of the user's expenses

    Returns:
        bar_chart: Bar chart representing spending distribution
    """
    bar_chart = Figure()
    bar_chart_axes = bar_chart.add_subplot(111)

    categories = {}
    for expense in expenses:
        category = expense[CATEGORY_INDEX]
        amount = expense[AMOUNT_INDEX]

        # Gathering categories that expenses used
        if category not in categories.keys():
            categories[category] = 0


        # Sum up number of times categories and payment methods were used
        categories[category] += amount

    spending = dict(sorted(categories.items(), key=lambda item: item[1]))
    y_axes = np.arange(len(spending.keys()))
    x_axes = np.arange(len(spending.values()))

    bar_chart_axes.set_title("Top Spending by Categories")
    bar_chart_axes.set_ylabel("Category")
    bar_chart_axes.set_xlabel("Amount")

    bar_chart_axes.barh(y_axes, x_axes)
    bar_chart_axes.set_yticks(y_axes, labels=spending.keys())
    bar_chart_axes.set_xticks(x_axes, labels=spending.values())

    return bar_chart