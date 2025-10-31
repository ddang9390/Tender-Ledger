# Author - Daniel Dang
# Filename - main_ui.py
# Purpose - Acts as the main window for the project

import tkinter
import customtkinter
from .Pages.expenses_page import ExpensesPage
from .Pages.dashboard_page import DashboardPage
from .Pages.profile_page import ProfilePage  
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

        self.page_container = customtkinter.CTkFrame(self)
        self.page_container.pack(side="top", fill="both", expand=True)
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid(row=0, column=1)
        

        # Setup navbar TODO - only display when logged in
        self.navbar = NavBar(self, self, db)
        self.navbar.grid(row=0, column=0, sticky="nsw")

        # Setup pages
        self.pages = {
            "ExpensesPage": ExpensesPage(self.page_container, self, db),
            "DashboardPage": DashboardPage(self.page_container, self, db),
            "ProfilePage": ProfilePage(self.page_container, self, db)
        }

        # Setup default page TODO - change to login
        self.show_page("ExpensesPage")

    def show_page(self, page):
        """
        Replace the current page with the new one

        Argument:
            page (String): The new page to be displayed
        """
        p = self.pages[page]

        p.grid(row=0, column=1, sticky="nsew")
        p.tkraise()

    