# Author - Daniel Dang
# Filename - user_form.py
# Purpose - Handles the appearance and logic of the user form

import re
import customtkinter
from tkcalendar import DateEntry
from ..Elements.password_field import PasswordField

class UserForm(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db, confirm_command, cancel_command, user=None):
        """
        Initializes a new instance of the LoginPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
            confirm_command: Command for confirm button
            cancel_command: Command for cancel button
            user (dict): Dictionary containing the user's info
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        if confirm_command and cancel_command:
            self.confirm_command = confirm_command
            self.cancel_command = cancel_command

        else:
            self.confirm_command = self.update_user()
            self.cancel_command = self.cancel()


        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        self.modify_mode = True

        # Register validation commands for user input
        self.validate_input_cmd = self.register(self.validate_phone_field)
        self.setup_inputs()
        
    def set_user(self, user):
        """
        Fill in the fields using the user's info

        Argument:
            user (dict): Dictionary containing the user's info
        """
        self.user = user
        self.modify_mode = False

    def setup_inputs(self):
        """
        Setup the input fields
        """
        # Setting up first name field
        first_name_label = customtkinter.CTkLabel(self.input_frame, text="First Name:")
        first_name_label.grid(row=2, column=0, pady=10, padx=10)
        self.firstname = customtkinter.CTkEntry(self.input_frame)
        self.firstname.grid(row=2, column=1, pady=10, padx=10)
        self.firstname.bind('<Return>', self.confirm_command)

        # Setting up last name field
        last_name_label = customtkinter.CTkLabel(self.input_frame, text="Last Name:")
        last_name_label.grid(row=3, column=0, pady=10, padx=10)
        self.lastname = customtkinter.CTkEntry(self.input_frame)
        self.lastname.grid(row=3, column=1, pady=10, padx=10)
        self.lastname.bind('<Return>', self.confirm_command)

        # Setting up birthday field
        birthday_label = customtkinter.CTkLabel(self.input_frame, text="Birthday:")
        birthday_label.grid(row=4, column=0, pady=10, padx=10)
        self.birthday = DateEntry(self.input_frame, selectmode='day', state='normal', showweeknumbers=False)
        self.birthday.grid(row=4, column=1, pady=10, padx=10)


        # Setting up username field
        username_label = customtkinter.CTkLabel(self.input_frame, text="Username *:")
        username_label.grid(row=5, column=0, pady=10, padx=10)
        self.username = customtkinter.CTkEntry(self.input_frame)
        self.username.grid(row=5, column=1, pady=10, padx=10)
        self.username.bind('<Return>', self.confirm_command)

        # Setting up password field
        password_label = customtkinter.CTkLabel(self.input_frame, text="Password *:")
        password_label.grid(row=6, column=0, pady=10, padx=10)
        self.password = PasswordField(self.input_frame, self.confirm_command)
        self.password.grid(row=6, column=1, pady=10, padx=10)

        # Setting up confirm password field 
        confirm_password_label = customtkinter.CTkLabel(self.input_frame, text="Confirm Password:")
        confirm_password_label.grid(row=7, column=0, pady=10, padx=10)
        self.confirm_password = PasswordField(self.input_frame, self.confirm_command)
        self.confirm_password.grid(row=7, column=1, pady=10, padx=10)

        # Setting up email field
        email_label = customtkinter.CTkLabel(self.input_frame, text="Email *:")
        email_label.grid(row=8, column=0, pady=10, padx=10)
        self.email = customtkinter.CTkEntry(self.input_frame)
        self.email.grid(row=8, column=1, pady=10, padx=10)
        self.email.bind('<Return>', self.confirm_command)

        # Setting up phone field
        phone_label = customtkinter.CTkLabel(self.input_frame, text="Phone *:")
        phone_label.grid(row=9, column=0, pady=10, padx=10)
        self.phone = customtkinter.CTkEntry(
            self.input_frame,
            validate="key",
            validatecommand=(self.validate_input_cmd, '%P'))
        self.phone.grid(row=9, column=1, pady=10, padx=10)
        self.phone.bind('<Return>', self.confirm_command)


        # Add confirm button
        login_button = customtkinter.CTkButton(self.input_frame, text="Register", command=self.confirm_command)
        login_button.grid(row=10, column=1, padx=20, pady=20)

        # Add Cancel button
        register_button = customtkinter.CTkButton(self.input_frame, text="Cancel", command=self.cancel_command)
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
            int(val)

            # Keep phone number within correct length
            if len(val) > 10:
                return False
            
            return True
        
        except ValueError:
            return False

    def update_user(self):
        """
        Updates the user's info using what is in the form
        """
        pass

    def cancel(self):
        """
        Return to the profile view page
        """
        pass