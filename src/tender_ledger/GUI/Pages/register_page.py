# Author - Daniel Dang
# Filename - register_page.py
# Purpose - Handles the appearance and logic of the register page

import customtkinter
from ...Backend.users import add_user, get_user_by_username
from ...Backend.password_utils import hash_password
from ..Elements.error_message import ErrorMessage
from ..Elements.user_form import UserForm

class RegisterPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the LoginPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        # Making row and column spacers to center register frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1) 

        self.register_frame = customtkinter.CTkFrame(
            self, 
            border_width=2, 
            border_color="gray",
            corner_radius=10
        )
        self.register_frame.grid(row=1, column=1, sticky="nsew")

        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id

        # Setup error message
        self.error_message = ErrorMessage(self.register_frame, self.controller)
        self.error_message.hide()
        
        # Setup Header
        label = customtkinter.CTkLabel(self.register_frame, text="Register", font=self.controller.font_label)
        label.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)

        # Setup user form
        self.user_form = UserForm(self.register_frame, self.controller, self.db, self.register_user, self.login)
        self.user_form.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0,20))

    def register_user(self, event=None):
        """
        Logs the user in if there is a matching username and password combination

        Argument:
            event: Key press event for pressing enter
        """
        username = self.user_form.username.get()
        password = self.user_form.password.get()
        first_name = self.user_form.firstname.get()
        last_name = self.user_form.lastname.get()
        birthday = self.user_form.birthday.get()
        email = self.user_form.email.get()
        phone = self.user_form.phone.get()
        confirm_password = self.user_form.confirm_password.get()

        # See if username is a duplicate
        if get_user_by_username(username, self.db):
            self.error_message.show(row=1, col=1, message="The username already exists")
            return

        if password != confirm_password:
            self.error_message.show(row=1, col=1, message="Passwords must match")

        elif username == "" or password == "" or email == "" or phone == "":
            self.error_message.show(row=1, col=1, message="Please fill in all fields")

        elif not self.user_form.is_valid_email(email):
            self.error_message.show(row=1, col=1, message="Invalid email")

        elif len(phone) != 10:
            self.error_message.show(row=1, col=1, message="Invalid phone")

        else:
            password = hash_password(password)
            add_user(username, password, first_name, last_name, birthday, email, phone, self.db)
            self.controller.show_message("Successfully registered user")
            self.controller.show_page("LoginPage")

    def login(self):
        """
        Return to the login page
        """
        self.error_message.hide()
        self.controller.show_page("LoginPage")
