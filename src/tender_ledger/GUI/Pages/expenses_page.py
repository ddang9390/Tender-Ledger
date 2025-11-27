# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter

from ..Elements.Expenses.add_expense_popup import AddExpensePopup
from ..Elements.Expenses.expense_table import ExpenseTable
from ..Elements.confirmation_popup import ConfirmationPopup
from ..Elements.filter_section import FilterSection 
from ...Backend.categories import get_categories_for_user
from ...Backend.payment_methods import get_payment_methods_for_user
from ...Backend.csv_utils import download_expenses_csv, import_expenses_csv

class ExpensesPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ExpensesPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        # Have elements in main container expand properly
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
 
        
    def refresh_page(self, user_id):
        """
        Updates the page
        
        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id

        self.categories = get_categories_for_user(self.user_id, self.db)
        self.payment_methods = get_payment_methods_for_user(self.user_id, self.db)
        
        
        # Creating header section
        label = customtkinter.CTkLabel(self, text="My Expenses", font=self.controller.font_label)
        label.grid(row=0, column=0, sticky="w")

        download_button = customtkinter.CTkButton(self, text="Download", command=self.download_csv)
        download_button.grid(row=0, column=1, sticky="e")

        add_button = customtkinter.CTkButton(self, text="Add", command=self.display_popup)
        add_button.grid(row=0, column=2, sticky="e")

        # Creating filter section
        self.filter_frame = customtkinter.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, columnspan=3, pady=20, sticky="nsew")
        self.filter_section = FilterSection(self.filter_frame, self, True)

        # Creating table
        self.expense_table_frame = customtkinter.CTkFrame(self) 
        self.expense_table_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.expense_table = ExpenseTable(self.expense_table_frame, self, self.filter_section, self.db)

    def display_popup(self, deleting=None, editing=None):
        """
        Displays the popup for adding or deleting expenses

        Argument:
            deleting (tuple): First element contains type being deleted, second contains ID
            editing (int): Contains ID of expense to edit
        """
        if not deleting and not editing:
            popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=self.categories, payment_methods=self.payment_methods, expense_page=self, db=self.db)
        
        elif editing:
            popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=self.categories, payment_methods=self.payment_methods, expense_page=self, db=self.db, editing=editing)
        else:
            popup = ConfirmationPopup(parent=self.parent, controller=self.controller,db=self.db, action=deleting)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)

    def refresh_table(self):
        """
        Refresh the expenses table
        """
        self.expense_table.refresh_table()

    def download_csv(self):
        """
        Downloads a csv file using the expenses in the table
        """
        # Remove the last values from the expenses which were their ids
        to_download = [list(expense[:-1]) for expense in self.expense_table.expenses]

        # Formatting data by reordering the columns
        for expense in to_download:
            expense[0], expense[1] = expense[1], expense[0]
            expense[2], expense[3] = expense[3], expense[2]

        download_expenses_csv(to_download)

        self.controller.show_message("Successfully downloaded expenses")

    def import_csv(self):
        """
        Import a csv file and add them to the user's expenses
        """
        print("importing")