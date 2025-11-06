# Author - Daniel Dang
# Filename - dashboard.py
# Purpose - Generates the charts for the dashboard

from matplotlib.figure import Figure


# Defining constants which are the indices of the elements that
# appear in the expenses list
CATEGORY_INDEX = 3
PAYMENT_METHOD_INDEX = 2

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
    category_pie_axes.pie(categories.values(), labels = categories.keys())
    category_pie_axes.set_title('Distribution by Categories')

    # Making pie chart for distribution by payment methods
    payment_method_pie = Figure()
    payment_method_pie_axes = payment_method_pie.add_subplot(111)
    payment_method_pie_axes.pie(payment_methods.values(), labels = payment_methods.keys())
    payment_method_pie_axes.set_title('Distribution by Payment Methods')
    
    return category_pie, payment_method_pie