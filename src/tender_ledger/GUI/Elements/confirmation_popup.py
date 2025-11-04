# Author - Daniel Dang
# Filename - confirmation_popup.py
# Purpose - Handles the appearance and fucntion of the confirmation popup

import sqlite3
import customtkinter
from ...Backend.expenses import delete_expense

# Defining constants
ADD_TITLE = "Add Expense"
UPDATE_TITLE = "Edit Expense"

TITLES = {
    "Expense": "Delete Expense",
    "User": "Delete User",
    "Category": "Delete Category",
    "Payment Method": "Delete Payment Method"
}

class ConfirmationPopup(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, db, action):
        """
        Initializes a new instance of the ProfilePage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
            action (tuple): First element contains type being deleted, second contains ID, third contains the page the action is from
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db
        self.action = action

        self.center_window()

        # Set title according to type of action
        self.title(TITLES[action[0]])

        # Set message
        message = customtkinter.CTkLabel(self, text="Are you sure?")
        message.grid(row=0)

        # Setting up inputs and buttons
        self.setup_buttons()

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



    def setup_buttons(self):
        """
        Set up the buttons for the confirmation popup
        """
        # Setting up overall display of button frame
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0, pady=10)

        add_button = customtkinter.CTkButton(button_frame, text="Confirm", command=self.execute_action)
        add_button.pack(side="right", padx=10)
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=10)


    def execute_action(self):
        """
        Executes the action (for now it is just deleting expenses)

        #TODO - expand to handle deleting other types
        """
        delete_expense(self.action[1], self.db)
        self.action[2].refresh_table()
        self.destroy()
            