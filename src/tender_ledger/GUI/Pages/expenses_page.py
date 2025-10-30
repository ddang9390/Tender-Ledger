# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter
from ..Elements.add_expense_popup import AddExpensePopup
from ...Backend.categories import get_categories_for_user

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

        label = customtkinter.CTkLabel(self, text="My Expenses")
        label.pack()

        add_button = customtkinter.CTkButton(self, text="Add", command=self.display_popup)
        add_button.pack()

    def display_popup(self):
        """
        Displays the popup for adding new expenses
        """
        #TODO - change user id once login functionality is implemented
        user_id = -1
        categories = get_categories_for_user(user_id, self.db)
        print(categories)

        popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=categories, db=self.db)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)