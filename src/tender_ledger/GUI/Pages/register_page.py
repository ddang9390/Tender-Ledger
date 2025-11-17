# Author - Daniel Dang
# Filename - register_page.py
# Purpose - Handles the appearance and logic of the register page

import customtkinter
import re
from tkcalendar import DateEntry
from ...Backend.users import add_user, get_user_by_username
from ...Backend.password_utils import hash_password
from ..Elements.error_message import ErrorMessage
from ..Elements.password_field import PasswordField

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


        # Register validation commands for user input
        self.validate_input_cmd = self.register(self.validate_phone_field)
        
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

    ###########################################
    # TODO - move stuff in between lines of # to another file so that this can be reused for the profile page
    def setup_inputs(self):
        """
        Setup the input fields
        """
        # Setting up first name field
        first_name_label = customtkinter.CTkLabel(self, text="First Name:")
        first_name_label.grid(row=2, column=0, pady=10, padx=10)
        self.firstname = customtkinter.CTkEntry(self)
        self.firstname.grid(row=2, column=1, pady=10, padx=10)
        self.firstname.bind('<Return>', lambda x:self.register_user())

        # Setting up last name field
        last_name_label = customtkinter.CTkLabel(self, text="Last Name:")
        last_name_label.grid(row=3, column=0, pady=10, padx=10)
        self.lastname = customtkinter.CTkEntry(self)
        self.lastname.grid(row=3, column=1, pady=10, padx=10)
        self.lastname.bind('<Return>', lambda x:self.register_user())

        # Setting up birthday field
        birthday_label = customtkinter.CTkLabel(self, text="Birthday:")
        birthday_label.grid(row=4, column=0, pady=10, padx=10)
        self.birthday = DateEntry(self, selectmode='day', state='normal', showweeknumbers=False)
        self.birthday.grid(row=4, column=1, pady=10, padx=10)


        # Setting up username field
        username_label = customtkinter.CTkLabel(self, text="Username *:")
        username_label.grid(row=5, column=0, pady=10, padx=10)
        self.username = customtkinter.CTkEntry(self)
        self.username.grid(row=5, column=1, pady=10, padx=10)
        self.username.bind('<Return>', lambda x:self.register_user())

        # Setting up password field
        password_label = customtkinter.CTkLabel(self, text="Password *:")
        password_label.grid(row=6, column=0, pady=10, padx=10)
        self.password = PasswordField(self, self.register_user)
        self.password.grid(row=6, column=1, pady=10, padx=10)

        # Setting up confirm password field 
        confirm_password_label = customtkinter.CTkLabel(self, text="Confirm Password:")
        confirm_password_label.grid(row=7, column=0, pady=10, padx=10)
        self.confirm_password = PasswordField(self, self.register_user)
        self.confirm_password.grid(row=7, column=1, pady=10, padx=10)

        # Setting up email field
        email_label = customtkinter.CTkLabel(self, text="Email *:")
        email_label.grid(row=8, column=0, pady=10, padx=10)
        self.email = customtkinter.CTkEntry(self)
        self.email.grid(row=8, column=1, pady=10, padx=10)
        self.email.bind('<Return>', lambda x:self.register_user())

        # Setting up phone field
        phone_label = customtkinter.CTkLabel(self, text="Phone *:")
        phone_label.grid(row=9, column=0, pady=10, padx=10)
        self.phone = customtkinter.CTkEntry(
            self,
            validate="key",
            validatecommand=(self.validate_input_cmd, '%P'))
        self.phone.grid(row=9, column=1, pady=10, padx=10)
        self.phone.bind('<Return>', lambda x:self.register_user())


        # Add confirm button
        login_button = customtkinter.CTkButton(self, text="Register", command=self.register_user)
        login_button.grid(row=10, column=1, padx=20, pady=20)

        # Add Cancel button
        register_button = customtkinter.CTkButton(self, text="Cancel", command=self.login)
        register_button.grid(row=11, column=1, padx=20, pady=20)

    def is_valid_email(self, email):
        """
        Checks if the inputted email is valid

        Returns:
            bool: True if the input is a valid email
                  False if not
        """
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(regex, email):
            return True
        
        return False

    def validate_phone_field(self, val):
        """
        Ensures that the Phone field only accepts numbers

        Returns:
            bool: True if the input is a valid number
                  False if not
        """
        # Allow the field to be empty
        if val == "":
            return True

        try:
            # Check if the value is a valid float
            new_val = int(val)

            # Keep phone number within correct length
            if len(self.phone.get()) > 9:
                return False
            
            return True
        
        except ValueError:
            return False
        

        
    #####################################

    def register_user(self, event=None):
        """
        Logs the user in if there is a matching username and password combination

        Argument:
            event: Key press event for pressing enter
        """
        username = self.username.get()
        password = self.password.get()
        first_name = self.firstname.get()
        last_name = self.lastname.get()
        birthday = self.birthday.get()
        email = self.email.get()
        phone = self.phone.get()
        confirm_password = self.confirm_password.get()

        # See if username is a duplicate
        if get_user_by_username(username, self.db):
            self.error_message.show(row=1, col=1, message="The username already exists")
            return

        if password != confirm_password:
            self.error_message.show(row=1, col=1, message="Passwords must match")

        elif username == "" or password == "" or email == "" or phone == "":
            self.error_message.show(row=1, col=1, message="Please fill in all fields")

        elif not self.is_valid_email(email):
            self.error_message.show(row=1, col=1, message="Invalid email")

        elif len(phone) != 10:
            self.error_message.show(row=1, col=1, message="Invalid phone")

        else:
            password = hash_password(password)
            add_user(username, password, first_name, last_name, birthday, email, phone, self.db)
            self.controller.show_page("LoginPage")

    def login(self):
        """
        Return to the login page
        """
        self.error_message.hide()
        self.controller.show_page("LoginPage")
