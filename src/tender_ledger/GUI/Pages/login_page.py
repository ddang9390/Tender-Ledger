# Author - Daniel Dang
# Filename - login.py
# Purpose - Handles the appearance and logic of the login page

import customtkinter
from ...Backend.users import get_user

class LoginPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the LoginPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db


        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id
        
        # Make widths of columns the same
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_columnconfigure(2, weight=1, uniform="group1")
        
        # Setup Header
        label = customtkinter.CTkLabel(self, text="Login", font=self.controller.font_label)
        label.grid(row=0, column=1, sticky="nsew")

        self.setup_inputs()

        # Setup register link

    def setup_inputs(self):
        """
        Setup the input fields
        """
        # Setting up username field
        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.grid(row=1, column=0, pady=10, padx=10)
        self.username = customtkinter.CTkEntry(self)
        self.username.grid(row=1, column=1, pady=10, padx=10)

        # Setting up password field
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=2, column=0, pady=10, padx=10)
        self.password = customtkinter.CTkEntry(self, show="*")
        self.password.grid(row=2, column=1, pady=10, padx=10)

        # Add confirm button
        login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        login_button.grid(row=3, column=1, padx=20, pady=20)

    def login(self):
        """
        Logs the user in if there is a matching username and password combination
        """
        username = self.username.get()
        password = self.password.get()


        user = get_user(username, password, self.db)

        if len(user) > 0:
            self.controller.user_id = user[0][0]
            self.controller.show_page("DashboardPage")