# Author - Daniel Dang
# Filename - add_expense_popup.py
# Purpose - Handles the appearance and fucntion of the Add Expense popup

import sqlite3
import customtkinter
from tkcalendar import DateEntry
from ...Backend.expenses import add_expense, update_expense

# Defining constants
ADD_TITLE = "Add Expense"
UPDATE_TITLE = "Edit Expense"

DB_DIR = "data"
DB_NAME = "tender_ledger.db"
DB_PATH = DB_DIR + "/" + DB_NAME

class AddExpensePopup(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, categories, db, editing=False):
        """
        Initializes a new instance of the ProfilePage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            categories (dict): Contains names of categories as values and ids as keys
            db (DatabaseManager): Instance of database manager being used
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.categories = categories
        self.db = db

        if editing:
            self.title(UPDATE_TITLE)
        else:
            self.title(ADD_TITLE)
            

        self.setup_inputs()
        self.setup_buttons(editing)

        

    def setup_inputs(self):
        """
        Set up the input fields for adding/updating expenses
        """
        # Setting up overall display of input frame
        input_frame = customtkinter.CTkFrame(self)
        input_frame.grid(row=0, column=0, sticky="nsew")

        # Setting up date field
        date_label = customtkinter.CTkLabel(input_frame, text="Date:")
        date_label.grid(row=0, column=0)
        self.date = DateEntry(input_frame, selectmode='day')
        self.date.grid(row=0, column=1)

        # Setting up amount field
        amount_label = customtkinter.CTkLabel(input_frame, text="Amount:")
        amount_label.grid(row=1, column=0)
        self.amount = customtkinter.CTkEntry(input_frame)
        self.amount.grid(row=1, column=1)

        # Setting up category field
        categories = []
        for category in self.categories.keys():
            categories.append(category)
        category_label = customtkinter.CTkLabel(input_frame, text="Category:")
        category_label.grid(row=2, column=0)
        self.category = customtkinter.CTkOptionMenu(input_frame, values=categories)
        self.category.grid(row=2, column= 1)

        # Setting up Method of Purchase field
        method_of_purchase = ["hi", "ha"]
        method_label = customtkinter.CTkLabel(input_frame, text="Method of Purchase:")
        method_label.grid(row=3, column=0)
        self.method = customtkinter.CTkOptionMenu(input_frame, values=method_of_purchase)
        self.method.grid(row=3, column= 1)

        # Setting up Location field
        location_label = customtkinter.CTkLabel(input_frame, text="Location:")
        location_label.grid(row=4, column=0)
        self.location = customtkinter.CTkEntry(input_frame)
        self.location.grid(row=4, column=1)

    def setup_buttons(self, editing):
        """
        Set up the buttons for the expense popup

        Argument:
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        # Setting up overall display of button frame
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0)

        add_button = customtkinter.CTkButton(button_frame, text="Add", command=self.add_expense)
        add_button.pack(side="right")
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left")


    def add_expense(self):
        """
        Adds the expense when all required fields are filled out
        """
        #TODO - change user id to actual user's id once login function is implemented
        user_id = -1

        amount = self.amount.get()
        date_of_purchase = self.date.get_date()
        payment_method_id = self.method.get() 
        category_id = self.categories[self.category.get()]
        location = self.location.get()
 

        add_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, self.db)
        self.destroy()
            