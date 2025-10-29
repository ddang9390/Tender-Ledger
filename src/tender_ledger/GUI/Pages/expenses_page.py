# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter
from ..Elements.add_expense_popup import AddExpensePopup

class ExpensesPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        """
        Initializes a new instance of the ExpensesPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="My Expenses")
        label.pack()

        add_button = customtkinter.CTkButton(self, text="Add", command=self.display_popup)
        add_button.pack()

    def display_popup(self):
        """
        Displays the popup for adding new expenses
        """
        popup = AddExpensePopup(parent=self.parent, controller=self.controller)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)