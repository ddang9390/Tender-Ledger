# Author - Daniel Dang
# Filename - dashboard.py
# Purpose - Generates the charts for the dashboard

import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from matplotlib.figure import Figure

# Defining constants which are the indices of the elements that
# appear in the expenses list
CATEGORY_INDEX = 3
PAYMENT_METHOD_INDEX = 2
AMOUNT_INDEX = 0

# Styling Constants to have colors of graphs match customtkinter color scheme
TEXT_COLOR = 'white'
FACE_COLOR = '#2B2B2B'
ACCENT_COLOR = '#3B8ED0'

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
        category = expense[CATEGORY_INDEX]  if expense[CATEGORY_INDEX] is not None else "Uncategorized"
        payment_method = expense[PAYMENT_METHOD_INDEX]  if expense[PAYMENT_METHOD_INDEX] is not None else "Uncategorized"
        amount = expense[AMOUNT_INDEX]

        # Adding up values by expense amounts
        categories[category] = categories.get(category, 0) + amount
        payment_methods[payment_method] = payment_methods.get(payment_method, 0) + amount

    # Making pie chart for distribution by categories
    category_pie = Figure(figsize=(4, 3), facecolor=FACE_COLOR)
    category_pie_axes = category_pie.add_subplot(111)
    category_pie_axes.pie(categories.values(), labels = categories.keys(), autopct='%1.1f%%', textprops={'color': TEXT_COLOR})
    category_pie_axes.set_title('Distribution by Categories', color=TEXT_COLOR)

    # Making pie chart for distribution by payment methods
    payment_method_pie = Figure(figsize=(4, 3), facecolor=FACE_COLOR)
    payment_method_pie_axes = payment_method_pie.add_subplot(111)
    payment_method_pie_axes.pie(payment_methods.values(), labels = payment_methods.keys(), autopct='%1.1f%%', textprops={'color': TEXT_COLOR})
    payment_method_pie_axes.set_title('Distribution by Payment Methods', color=TEXT_COLOR)
    
    category_pie.tight_layout()
    payment_method_pie.tight_layout()

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
    line_plot = Figure(figsize=(4, 3), facecolor=FACE_COLOR)
    line_plot_axes = line_plot.add_subplot(111)
    line_plot_axes.set_facecolor(FACE_COLOR)

    dates = list(sorted_spending.keys())
    if dates:
        line_plot_axes.plot(dates, sorted_spending.values(), marker='o', linestyle='-', color=ACCENT_COLOR, linewidth=2)

        # Format the dates
        date_fmt = mdates.DateFormatter('%b %d')
        line_plot_axes.xaxis.set_major_formatter(date_fmt)
        line_plot.autofmt_xdate()

        # Add grid
        line_plot_axes.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    line_plot_axes.set_title("Daily Spending", color=TEXT_COLOR)
    line_plot_axes.set_xlabel("Dates", color=TEXT_COLOR)
    line_plot_axes.set_ylabel("Amount", color=TEXT_COLOR)

    line_plot_axes.tick_params(axis='x', labelrotation=45, color=TEXT_COLOR, labelcolor=TEXT_COLOR)
    line_plot_axes.tick_params(axis='y', color=TEXT_COLOR, labelcolor=TEXT_COLOR)

    for spine in line_plot_axes.spines.values():
        spine.set_edgecolor(TEXT_COLOR)

    line_plot.tight_layout()

    return line_plot

def generate_bar_chart(expenses):
    """
    Generates a horizontal bar chart showing the ranking of categories by total spending

    Argument:
        expenses (List): List of the user's expenses

    Returns:
        bar_chart: Bar chart representing spending distribution
    """
    bar_chart = Figure(figsize=(4, 3), facecolor=FACE_COLOR)
    bar_chart_axes = bar_chart.add_subplot(111)
    bar_chart_axes.set_facecolor(FACE_COLOR)

    categories = {}
    for expense in expenses:
        category = expense[CATEGORY_INDEX] if expense[CATEGORY_INDEX] is not None else "Uncategorized"
        amount = expense[AMOUNT_INDEX]

        # Sum up number of times categories and payment methods were used
        categories[category] = categories.get(category, 0) + amount

    # Sort categories
    spending = dict(sorted(categories.items(), key=lambda item: item[1]))
    cat_names = list(spending.keys())
    cat_amounts = list(spending.values())

    if cat_amounts:
        bar_chart_axes.barh(cat_names, cat_amounts, color=ACCENT_COLOR)

        # Format amounts
        amount_fmt = mtick.StrMethodFormatter("${x:,.0f}")
        bar_chart_axes.xaxis.set_major_formatter(amount_fmt)

        # Add vertical lines to chart
        bar_chart_axes.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.5, axis='x')

    bar_chart_axes.set_title("Top Spending by Categories", color=TEXT_COLOR)
    bar_chart_axes.set_xlabel("Amount", color=TEXT_COLOR)

    bar_chart_axes.tick_params(axis='x', colors=TEXT_COLOR)
    bar_chart_axes.tick_params(axis='y', colors=TEXT_COLOR)
    for spine in bar_chart_axes.spines.values():
        spine.set_edgecolor(TEXT_COLOR)

    bar_chart.tight_layout()

    return bar_chart