# Author - Daniel Dang
# Filename - error_message.py
# Purpose - Handles the appearance of the customization section from the Profile page

import customtkinter
from ...Backend.categories import get_categories_for_user
from ...Backend.payment_methods import get_payment_methods_for_user
from tkinter import ttk

class Customizations(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ProfilePage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        self.customizations_frame = customtkinter.CTkFrame(self)
        self.customizations_frame.grid(row=0, column=0, sticky="nsew")
        

    def set_user(self, user_id):
        """
        Fill in the fields using the user's info

        Argument:
            user_id (int): The user's ID
        """
        self.user_id = user_id
        self.setup_lists()


    def setup_lists(self):
        """
        Setup the lists for the Categories and Payment Methods
        """
        self.setup_categories()
        self.setup_payment_methods()

    def setup_categories(self):
        """
        Setup the Categories list
        """
        categories = get_categories_for_user(self.user_id, self.db)
        print(categories)
        label = customtkinter.CTkLabel(self.customizations_frame, text="Categories")
        label.grid(row=0, column=0)

        # Adding columns to table
        columns = ('date', 'amount', 'category', 'payment method', 'location', 'edit', 'delete')
        self.category_table = ttk.Treeview(self.customizations_frame, columns=columns, show='headings')

        # Add headers to columns
        self.category_table.heading('date', text='Date')
        self.category_table.heading('amount', text='Amount')
        self.category_table.heading('category', text='Category')
        self.category_table.heading('payment method', text='Payment Method')
        self.category_table.heading('location', text='Location')
        self.category_table.heading('edit', text="Edit")
        self.category_table.heading('delete', text="Delete")

    def setup_payment_methods(self):
        """
        Setup the Payment Methods list
        """
        methods = get_payment_methods_for_user(self.user_id, self.db)
        print(methods)
        label = customtkinter.CTkLabel(self.customizations_frame, text="Payment Methods")
        label.grid(row=0, column=1)