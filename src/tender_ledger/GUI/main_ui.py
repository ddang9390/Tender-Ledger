# Author - Daniel Dang
# Filename - main_ui.py
# Purpose - Acts as the main window for the project

import customtkinter
from pathlib import Path
from .Pages.expenses_page import ExpensesPage
from .Pages.dashboard_page import DashboardPage
from .Pages.profile_page import ProfilePage  
from .Pages.login_page import LoginPage
from .Pages.register_page import RegisterPage
from .Elements.navbar import NavBar
from ..Backend.path_utils import get_theme_path

# Constants (might allow for custom resolutions later)
RESOLUTION_WIDTH = 1100
RESOLUTION_HEIGHT = 580

#ROOT_DIR = Path(__file__).parent
#THEME_FILE = ROOT_DIR / 'theme.json'

class App(customtkinter.CTk):
    def __init__(self, db):
        """
        Initializes the main UI for the project
        
        Argument:
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__()
        self.db = db

        # Setting global theme for visual appearance
        # TODO - actually change the values in the file
        theme = get_theme_path()
        customtkinter.set_default_color_theme(theme)
        
        self.set_styles()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) 

        self.title("Tender Ledger")
        self.center_window()

        #self.user_id = -1
        self.user_id = None
        self.navbar = NavBar(self, self, self.db)

        # Setup pages
        self.page_container = customtkinter.CTkFrame(self)
        self.page_container.pack(side="top", fill="both", expand=True)
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid(row=0, column=1)


        self.pages = {
            "ExpensesPage": ExpensesPage(self.page_container, self, db),
            "DashboardPage": DashboardPage(self.page_container, self, db),
            "ProfilePage": ProfilePage(self.page_container, self, db),
            "LoginPage": LoginPage(self.page_container, self, db),
            "RegisterPage": RegisterPage(self.page_container, self, db)
        }

        # Setup default page TODO - change to login
        self.show_page("LoginPage")

    def show_navbar(self):
        self.navbar.grid(row=0, column=0, sticky="nsw")

    def show_page(self, page):
        """
        Replace the current page with the new one

        Argument:
            page (String): The new page to be displayed
        """
        p = self.pages[page]

        # Show or hide the navbar
        if self.user_id:
            self.show_navbar()
            self.page_container.grid(row=0, column=1)
            self.grid_columnconfigure(0, weight=0)
            
        else:
            self.navbar.grid_forget()
            self.page_container.grid(row=0, column=0, sticky="nsew")
            self.grid_columnconfigure(0, weight=1)


        p.refresh_page(self.user_id)
        p.grid(row=0, column=1, sticky="nsew")
        p.tkraise()

    def center_window(self):
        """
        Center the window of the main app

        # TODO - place this function in some utils file so that the popups can use this instead
        """
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int((width/2) - (RESOLUTION_WIDTH/2))
        y = int((height/2) - (RESOLUTION_HEIGHT/1.5))

        # Launch window of custom resolution in center of screen
        self.geometry(f"{RESOLUTION_WIDTH}x{RESOLUTION_HEIGHT}+{x}+{y}")

    def set_styles(self):
        """
        Define styles to be used by certain parts of the app
        """
        self.font_label = customtkinter.CTkFont(family="Roboto", size=18, weight="bold")