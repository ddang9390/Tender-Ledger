# Author - Daniel Dang
# Filename - login.py
# Purpose - Handles the appearance and logic of the login page

import customtkinter
from ...Backend.users import get_user_by_username
from ...Backend.password_utils import verify_password
from ..Elements.error_message import ErrorMessage
from ..Elements.password_field import PasswordField


class LoginPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the LoginPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        #TODO - make login frame with a border

        self.showing = False

        
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
        label = customtkinter.CTkLabel(self, text="Login", font=self.controller.font_label)
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
        self.username.bind('<Return>', lambda x:self.login())

        # Setting up password field
        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.grid(row=3, column=0, pady=10, padx=10)
        self.password = PasswordField(self, self.login)
        self.password.grid(row=3, column=1, pady=10, padx=10)

        # Add confirm button
        login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        login_button.grid(row=4, column=1, padx=20, pady=20)

        # Add Register button
        register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        register_button.grid(row=5, column=1, padx=20, pady=20)

    

    def login(self, event=None):
        """
        Logs the user in if there is a matching username and password combination

        Argument:
            event: Key press event for pressing enter
        """
        username = self.username.get()
        password = self.password.get()

        user = get_user_by_username(username, self.db)
        if len(user) > 0:
            # Check if password is correct
            user_pw = user[0][2]
            if verify_password(password, user_pw):
                self.controller.user_id = user[0][0]
                self.controller.show_page("DashboardPage")
                return
        
        self.error_message.show(1, 1, "Invalid username or password")

    def register(self):
        """
        Go to the register page
        """
        self.error_message.hide()
        self.controller.show_page("RegisterPage")