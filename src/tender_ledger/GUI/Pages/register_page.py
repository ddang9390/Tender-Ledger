# Author - Daniel Dang
# Filename - register_page.py
# Purpose - Handles the appearance and logic of the register page

import customtkinter
from ...Backend.users import add_user
from ..Elements.error_message import ErrorMessage

class RegisterPage(customtkinter.CTkFrame):
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

        #TODO - make register frame with a border
        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id

        # Setup error message
        self.error_message = ErrorMessage(self, self.controller)
        self.error_message.hide()
        
        # Make widths of columns the same
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_columnconfigure(2, weight=1, uniform="group1")
        
        # Setup Header
        label = customtkinter.CTkLabel(self, text="Register", font=self.controller.font_label)
        label.grid(row=0, column=1, sticky="nsew")

        self.setup_inputs()



    def setup_inputs(self):
        """
        Setup the input fields
        """
        # Setting up username field
        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.grid(row=2, column=0, pady=10, padx=10)
        self.username = customtkinter.CTkEntry(self)
        self.username.grid(row=2, column=1, pady=10, padx=10)
        self.username.bind('<Return>', lambda x:self.register())

        # Setting up password field
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=3, column=0, pady=10, padx=10)
        self.password = customtkinter.CTkEntry(self, show="*")
        self.password.grid(row=3, column=1, pady=10, padx=10)
        self.password.bind('<Return>', lambda x:self.register())

        # Setting up confirm password field
        confirm_password_label = customtkinter.CTkLabel(self, text="Confirm Password:")
        confirm_password_label.grid(row=4, column=0, pady=10, padx=10)
        self.confirm_password = customtkinter.CTkEntry(self, show="*")
        self.confirm_password.grid(row=4, column=1, pady=10, padx=10)
        self.confirm_password.bind('<Return>', lambda x:self.register())

        # Add confirm button
        login_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        login_button.grid(row=5, column=1, padx=20, pady=20)

        # Add Cancel button
        register_button = customtkinter.CTkButton(self, text="Cancel", command=self.login)
        register_button.grid(row=6, column=1, padx=20, pady=20)

    def register(self):
        """
        Logs the user in if there is a matching username and password combination
        """
        username = self.username.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()

        if password != confirm_password:
            self.error_message.show(row=1, col=1, message="Passwords must match")

        elif username == "" or password == "":
            self.error_message.show(row=1, col=1, message="Please fill in all fields")

        else:
            add_user(username, password, self.db)
            self.controller.show_page("LoginPage")

    def login(self):
        """
        Return to the login page
        """
        self.error_message.hide()
        self.controller.show_page("LoginPage")
