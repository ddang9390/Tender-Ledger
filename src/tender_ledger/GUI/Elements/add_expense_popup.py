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
    def __init__(self, parent, controller, categories, payment_methods, db, expense_page, editing=False):
        """
        Initializes a new instance of the ProfilePage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            categories (dict): Contains names of categories as values and ids as keys
            db (DatabaseManager): Instance of database manager being used
            expense_page (ExpensePage): Instance of expense page being used
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.categories = categories
        self.payment_methods = payment_methods
        self.expense_page = expense_page
        self.db = db

        self.center_window()
        if editing:
            self.title(UPDATE_TITLE)
        else:
            self.title(ADD_TITLE)
            
        # Register validation commands for user input
        self.validate_input_cmd = self.register(self.validate_amount_input)

        # Setting up inputs and buttons
        self.setup_inputs()
        self.setup_buttons(editing)

    def center_window(self):
        """
        Ensures that the popup shows over the window rather than some random location
        """
        # Get dimensions of main window
        width = self.controller.winfo_width()
        height = self.controller.winfo_height()
        main_x = self.controller.winfo_x()
        main_y = self.controller.winfo_y()

        # Set coordinates of where popup should show
        x = main_x + (width // 2)
        y = (main_y//2) + (height // 2)

        self.geometry(f"+{x}+{y}")

    def setup_inputs(self):
        """
        Set up the input fields for adding/updating expenses
        """
        # Setting up overall display of input frame
        input_frame = customtkinter.CTkFrame(self)
        input_frame.grid(row=0, column=0, sticky="nsew")

        # Setting up date field
        date_label = customtkinter.CTkLabel(input_frame, text="Date:")
        date_label.grid(row=0, column=0, pady=10, padx=10)
        self.date = DateEntry(input_frame, selectmode='day', state='normal', showweeknumbers=False)
        self.date.grid(row=0, column=1, pady=10, padx=10)
        
        # Ensures that the DateEntry is at the top level to prevent clicking the fields behind it
        self.date._top_cal.transient(self)
        self.date._top_cal.lift()

        # Setting up amount field
        self.amount_label = customtkinter.CTkLabel(input_frame, text="Amount (*):")
        self.amount_label.grid(row=1, column=0, pady=10, padx=10)
        self.amount = customtkinter.CTkEntry(
            input_frame,
            validate="key",
            validatecommand=(self.validate_input_cmd, '%P')
        )
        self.amount.grid(row=1, column=1, pady=10, padx=10)

        # Setting up category field
        categories = []
        for category in self.categories.keys():
            categories.append(category)
        category_label = customtkinter.CTkLabel(input_frame, text="Category:")
        category_label.grid(row=2, column=0, pady=10)
        self.category = customtkinter.CTkOptionMenu(input_frame, values=categories)
        self.category.grid(row=2, column= 1, pady=10)

        # Setting up Method of Purchase field
        method_of_purchase = []
        for method in self.payment_methods.keys():
            method_of_purchase.append(method)
        method_label = customtkinter.CTkLabel(input_frame, text="Method of Purchase:")
        method_label.grid(row=3, column=0, pady=10, padx=10)
        self.method = customtkinter.CTkOptionMenu(input_frame, values=method_of_purchase)
        self.method.grid(row=3, column= 1, pady=10, padx=10)

        # Setting up Location field
        location_label = customtkinter.CTkLabel(input_frame, text="Location:")
        location_label.grid(row=4, column=0, pady=10, padx=10)
        self.location = customtkinter.CTkEntry(input_frame)
        self.location.grid(row=4, column=1, pady=10, padx=10)

    def validate_amount_input(self, val):
        """
        Ensures that the Amount field only accepts numbers with up to 2 decimal places

        Returns:
            bool: True if the input is a valid number
                  False if not
        """
        # Allow the field to be empty
        if val == "":
            return True

        try:
            # Check if the value is a valid float
            new_val = float(val)

            # Check if the value has more than 2 decimal places
            if "." in val and len(val.split('.')[1]) > 2:
                return False
            
            return True
        
        except ValueError:
            return False

    def setup_buttons(self, editing):
        """
        Set up the buttons for the expense popup

        Argument:
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        # Setting up overall display of button frame
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0, pady=10)

        add_button = customtkinter.CTkButton(button_frame, text="Add", command=self.add_expense)
        add_button.pack(side="right", padx=10)
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=10)


    def add_expense(self):
        """
        Adds the expense when all required fields are filled out
        """
        #TODO - change user id to actual user's id once login function is implemented
        user_id = -1

        amount = self.amount.get()
        date_of_purchase = self.date.get_date()
        payment_method_id = self.payment_methods[self.method.get()]
        category_id = self.categories[self.category.get()]
        location = self.location.get()
 
        if amount == "" or amount == None:
            self.amount_label.configure(text_color = "red")
        else:
            add_expense(user_id, amount, date_of_purchase, payment_method_id, category_id, location, self.db)
            self.expense_page.refresh_table()
            self.destroy()
            