# Author - Daniel Dang
# Filename - add_expense_popup.py
# Purpose - Handles the appearance and fucntion of the Add Expense popup

import datetime
import customtkinter
from tkcalendar import DateEntry
from ....Backend.expenses import add_expense, update_expense, get_expense
from ...Elements.error_message import ErrorMessage

# Defining constants
ADD_TITLE = "Add Expense"
UPDATE_TITLE = "Edit Expense"

DB_DIR = "data"
DB_NAME = "tender_ledger.db"
DB_PATH = DB_DIR + "/" + DB_NAME

class AddExpensePopup(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, categories, payment_methods, db, expense_page, editing=None):
        """
        Initializes a new instance of the Add Expense Popup

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            categories (dict): Contains names of categories as values and ids as keys
            payment_methods (dict): Contains names of payment methods as values and ids as keys
            db (DatabaseManager): Instance of database manager being used
            expense_page (ExpensePage): Instance of expense page being used
            editing (int): ID of the expense to edit
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.categories = categories
        self.payment_methods = payment_methods
        self.expense_page = expense_page
        self.db = db
        self.expense_to_edit = None

        # Position the popup and change its title
        self.center_window()
        if editing:
            self.title(UPDATE_TITLE)
            self.expense_to_edit = get_expense(editing, self.db)[0]
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

        # Setting up error message
        self.error_message = ErrorMessage(input_frame, self.controller)


        # Setting up date field
        date_label = customtkinter.CTkLabel(input_frame, text="Date:")
        date_label.grid(row=1, column=0, pady=10, padx=10)
        self.date = DateEntry(input_frame, selectmode='day', state='normal', showweeknumbers=False)
        self.date.grid(row=1, column=1, pady=10, padx=10)
        
        # Ensures that the DateEntry is at the top level to prevent clicking the fields behind it
        self.date._top_cal.transient(self)
        self.date._top_cal.lift()

        # Setting up amount field
        self.amount_label = customtkinter.CTkLabel(input_frame, text="Amount (*):")
        self.amount_label.grid(row=2, column=0, pady=10, padx=10)
        self.amount = customtkinter.CTkEntry(
            input_frame,
            validate="key",
            validatecommand=(self.validate_input_cmd, '%P')
        )
        self.amount.grid(row=2, column=1, pady=10, padx=10)

        # Setting up category field
        categories = []
        for category in self.categories.keys():
            categories.append(category)
        category_label = customtkinter.CTkLabel(input_frame, text="Category:")
        category_label.grid(row=3, column=0, pady=10)
        self.category = customtkinter.CTkOptionMenu(input_frame, values=categories)
        self.category.grid(row=3, column= 1, pady=10)

        # Setting up Method of Purchase field
        method_of_purchase = []
        for method in self.payment_methods.keys():
            method_of_purchase.append(method)
        method_label = customtkinter.CTkLabel(input_frame, text="Method of Purchase:")
        method_label.grid(row=4, column=0, pady=10, padx=10)
        self.method = customtkinter.CTkOptionMenu(input_frame, values=method_of_purchase)
        self.method.grid(row=4, column= 1, pady=10, padx=10)

        # Setting up Location field
        location_label = customtkinter.CTkLabel(input_frame, text="Location:")
        location_label.grid(row=5, column=0, pady=10, padx=10)
        self.location = customtkinter.CTkEntry(input_frame)
        self.location.grid(row=5, column=1, pady=10, padx=10)

        # Fill fields if editing an expense
        if self.expense_to_edit != None:
            # Formatting date so that it can be set properly
            date = datetime.datetime.strptime(self.expense_to_edit[1], "%Y-%m-%d").date()
            
            amount = customtkinter.StringVar(value=f"{self.expense_to_edit[0]:.2f}")
            category = self.expense_to_edit[3]
            payment_method = self.expense_to_edit[2]
            location = customtkinter.StringVar(value=self.expense_to_edit[4])

            self.date.set_date(date)
            self.category.set(category)
            self.amount.configure(textvariable=amount)
            self.method.set(payment_method)
            self.location.configure(textvariable=location)


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
        btn_label = "Add" if not editing else "Edit"

        # Setting up overall display of button frame
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0, pady=10)

        add_button = customtkinter.CTkButton(button_frame, text=btn_label, command=lambda: self.add_expense(editing))
        add_button.pack(side="right", padx=10)
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=10)


    def add_expense(self, editing):
        """
        Add or edit the expense when all required fields are filled out

        Argument:
            editing (int): ID of the expense to edit
        """
        amount = self.amount.get()
        date_of_purchase = self.date.get_date()
        payment_method_id = self.payment_methods[self.method.get()]
        category_id = self.categories[self.category.get()]
        location = self.location.get()
 
        if amount == "" or amount == None:
            self.amount_label.configure(text_color = "red")
            self.error_message.show(0, 0, "Please fill in all required fields", col_span=2)
        else:
            if not editing:
                add_expense(self.controller.user_id, amount, date_of_purchase, payment_method_id, category_id, location, self.db)
            else:
                update_expense(amount, date_of_purchase, payment_method_id, category_id, location, editing,self.db)
            self.expense_page.refresh_table()
            self.destroy()