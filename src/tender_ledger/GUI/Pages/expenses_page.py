# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter
from ..Elements.add_expense_popup import AddExpensePopup
from ...Backend.categories import get_categories_for_user
from ...Backend.payment_methods import get_payment_methods_for_user
from ...Backend.expenses import get_expenses_for_user
from tkinter import ttk

class ExpensesPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ExpensesPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        #TODO - change user id once login functionality is implemented
        user_id = -1
        self.categories = get_categories_for_user(user_id, self.db)
        self.payment_methods = get_payment_methods_for_user(user_id, self.db)
        self.expenses = get_expenses_for_user(user_id, self.db)
        
        

        label = customtkinter.CTkLabel(self, text="My Expenses")
        label.grid(row=0, column=0, sticky="w")

        add_button = customtkinter.CTkButton(self, text="Add", command=self.display_popup)
        add_button.grid(row=0, column=1, sticky="e")

        self.create_table()
        self.refresh_table()
        self.expense_table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        

    def display_popup(self):
        """
        Displays the popup for adding new expenses
        """
        popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=self.categories, payment_methods=self.payment_methods, db=self.db)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)

    def create_table(self):
        """
        Displays the table for the user's expenses
        """
        self.expense_table_frame = customtkinter.CTkFrame(self) 

        # Adding columns to table
        columns = ('date', 'amount', 'category', 'payment method', 'location', 'action')
        self.expense_table = ttk.Treeview(self.expense_table_frame, columns=columns, show='headings')

        # Add headers to columns
        self.expense_table.heading('date', text='Date')
        self.expense_table.heading('amount', text='Amount')
        self.expense_table.heading('category', text='Category')
        self.expense_table.heading('payment method', text='Payment Method')
        self.expense_table.heading('location', text='Location')
        self.expense_table.heading('action', text="Action")

        # Control column width
        self.expense_table.column('date', width=100)
        self.expense_table.column('amount', width=100)
        self.expense_table.column('category', width=100)
        self.expense_table.column('payment method', width=150)
        self.expense_table.column('location', width=200)
        self.expense_table.column('action', width=100)
        self.expense_table.grid(row=0, column=0, sticky="nsew")

    def refresh_table(self):
        """
        Refreshes the table by clearing it and then repopulating it
        """
        # Clear the table
        for row in self.expense_table.get_children():
            self.expense_table.delete(row)

        # Add expenses to the table
        for expense in self.expenses:
            display_values = (expense[1], expense[0], expense[3], expense[2], expense[4])
            self.expense_table.insert('', 'end', values=display_values)

    def edit_expense(self):
        """
        Opens the 'Add Expense' popup to edit the row's expense
        """
        print("Edit me")

    def delete_expense(self):
        """
        Shows a confirmation window for deleting the row's expense
        """
        print("delete me")