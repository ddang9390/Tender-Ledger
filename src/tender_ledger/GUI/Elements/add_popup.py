# Author - Daniel Dang
# Filename - add_popup.py
# Purpose - Handles the appearance and fucntion of the Add Expense popup

import datetime
import customtkinter

from ...Backend.categories import add_category, update_category, get_category
from ...Backend.payment_methods import add_payment_method, update_payment_method, get_payment_method
from ..Elements.error_message import ErrorMessage

# Defining constants
ADD_TITLES = {
    "Category": "Add Category",
    "Payment Method": "Add Payment Method"
}
UPDATE_TITLES = {
    "Category": "Edit Category",
    "Payment Method": "Edit Payment Method"
}

DB_DIR = "data"
DB_NAME = "tender_ledger.db"
DB_PATH = DB_DIR + "/" + DB_NAME

class AddPopup(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, db,  action, editing=None):
        """
        Initializes a new instance of the Add Expense Popup

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            categories (dict): Contains names of categories as values and ids as keys
            db (DatabaseManager): Instance of database manager being used
            action (String): Could be either 'Category' or 'Payment Method'
            editing (int): ID of the item to edit
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.action = action

        self.db = db
        self.to_edit = None

        # Position the popup and change its title
        self.center_window()
        if editing:
            self.title(UPDATE_TITLES[action])
            if action == 'Category':
                self.to_edit = get_category(editing, self.db)[0]
            else:
                self.to_edit = get_payment_method(editing, self.db)[0]
        else:
            self.title(ADD_TITLES[action])


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

        # Setting up Name field
        name_label = customtkinter.CTkLabel(input_frame, text="Name:")
        name_label.grid(row=5, column=0, pady=10, padx=10)
        self.name = customtkinter.CTkEntry(input_frame)
        self.name.grid(row=5, column=1, pady=10, padx=10)

        # Fill fields if editing an expense
        if self.to_edit != None:
            name = customtkinter.StringVar(value=self.to_edit[1])
            self.name.configure(textvariable=name)


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

        add_button = customtkinter.CTkButton(button_frame, text=btn_label, command=lambda: self.add(editing))
        add_button.pack(side="right", padx=10)
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=10)


    def add(self, editing):
        """
        Add or edit the category or payment method when all required fields are filled out

        Argument:
            editing (int): ID of the expense to edit
            
        """
        name = self.name.get()
 
        if name == "" or name == None:
            self.amount_label.configure(text_color = "red")
            self.error_message.show(0, 0, "Please fill in all required fields", col_span=2)
        else:
            if not editing:
                if self.action == 'Category':
                    if add_category(self.controller.user_id, name, self.db):
                        self.controller.show_message("Successfully added category")
                    else:
                        self.controller.show_message("Name already exists")
                        return
                elif self.action == 'Payment Method':
                    if add_payment_method(self.controller.user_id, name, self.db):
                        self.controller.show_message("Successfully added payment method")
                    else:
                        self.controller.show_message("Name already exists")
                        return
            else:
                if self.action == 'Category':
                    if update_category(editing, name, self.db):
                        self.controller.show_message("Successfully updated category")
                    else:
                        self.controller.show_message("Name already exists")
                        return
                elif self.action == 'Payment Method':
                    if update_payment_method(editing, name, self.db):
                        self.controller.show_message("Successfully updated payment method")
                    else:
                        self.controller.show_message("Name already exists")
                        return

            self.parent.refresh()
            self.destroy()