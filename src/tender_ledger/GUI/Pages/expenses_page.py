# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter

class ExpensesPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        """
        Initializes a new instance of the ExpensesPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
        """
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="My Expenses")
        label.pack()

        add_button = customtkinter.CTkButton(self, text="Add", command=self.add_expense)
        add_button.pack()

    def add_expense(self):
        """
        Displays the popup for adding new expenses
        """
        print("hello world")