# Author - Daniel Dang
# Filename - main_ui.py
# Purpose - Acts as the main window for the project

import tkinter
import customtkinter
from .Pages.expenses_page import ExpensesPage
from .Elements.navbar import NavBar

# Constants (might allow for custom resolutions later)
RESOLUTION_WIDTH = 1100
RESOLUTION_HEIGHT = 580

class App(customtkinter.CTk):
    def __init__(self, db):
        """
        Initializes the main UI for the project
        
        Argument:
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__()
        self.db = db

        self.title("Tender Ledger")
        self.geometry(f"{RESOLUTION_WIDTH}x{RESOLUTION_HEIGHT}")

        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Setup navbar TODO - only display when logged in
        self.navbar = NavBar(container, self, db)
        self.navbar.grid(row=0, column=0, sticky="nsw")

        # Setup default page TODO - change to login
        expenses_page = ExpensesPage(container, self, db)
        self.show_page(expenses_page)

    def show_page(self, page):
        """
        Replace the current page with the new one

        Argument:
            page: The new page to be displayed
        """
        page.grid(row=0, column=1, sticky="nsew")
        page.tkraise()

    