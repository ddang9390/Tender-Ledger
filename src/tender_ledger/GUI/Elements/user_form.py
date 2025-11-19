# Author - Daniel Dang
# Filename - user_form.py
# Purpose - Handles the appearance and logic of the user form

import re
import customtkinter
from tkcalendar import DateEntry
from ..Elements.password_field import PasswordField

class UserForm(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db, confirm_command, cancel_command, modify=True):
        """
        Initializes a new instance of the LoginPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
            confirm_command: Command for confirm button
            cancel_command: Command for cancel button
            modify (bool): True if the form is for adding or editing users
                           False if the form is just for viewing users
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        if confirm_command and cancel_command:
            self.confirm_command = confirm_command
            self.cancel_command = cancel_command

        else:
            self.confirm_command = self.update_user
            self.cancel_command = self.cancel


        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nsew")

        self.modify_mode = modify

        # Register validation commands for user input
        self.validate_input_cmd = self.register(self.validate_phone_field)

        self.user = None
        self.setup_inputs()
        
    def set_user(self, user):
        """
        Fill in the fields using the user's info

        Argument:
            user (dict): Dictionary containing the user's info
        """
        self.user = user
        self.modify_mode = False
        self.setup_inputs()

    def setup_inputs(self):
        """
        Setup the input fields
        """
        self.clear_form()

        if self.modify_mode:
            self.setup_modify_form()

        else:
            self.setup_view_form()
            

    def setup_input_fields(self):
        enable_entry = "normal" if self.modify_mode else "disabled"

        user_id = self.user["user_id"] if self.user else None
        username = customtkinter.StringVar(value=self.user["username"]) if self.user else None
        first_name = customtkinter.StringVar(value=self.user["first_name"]) if self.user else None
        last_name = customtkinter.StringVar(value=self.user["last_name"]) if self.user else None
        birthday = customtkinter.StringVar(value=self.user["birthday"]) if self.user else None
        email = customtkinter.StringVar(value=self.user["email"]) if self.user else None
        phone = customtkinter.StringVar(value=self.user["phone"]) if self.user else None

        # Setting up first name field
        first_name_label = customtkinter.CTkLabel(self.input_frame, text="First Name:")
        first_name_label.grid(row=2, column=0, pady=10, padx=10)
        self.firstname = customtkinter.CTkEntry(self.input_frame, textvariable=first_name, state=enable_entry)
        self.firstname.grid(row=2, column=1, pady=10, padx=10)
        self.firstname.bind('<Return>', self.confirm_command)

        # Setting up last name field
        last_name_label = customtkinter.CTkLabel(self.input_frame, text="Last Name:")
        last_name_label.grid(row=3, column=0, pady=10, padx=10)
        self.lastname = customtkinter.CTkEntry(self.input_frame, textvariable=last_name, state=enable_entry)
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
        self.username = customtkinter.CTkEntry(self.input_frame, textvariable=username, state=enable_entry)
        self.username.grid(row=5, column=1, pady=10, padx=10)
        self.username.bind('<Return>', self.confirm_command)

        if self.modify_mode:
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
        self.email = customtkinter.CTkEntry(self.input_frame, textvariable=email, state=enable_entry)
        self.email.grid(row=8, column=1, pady=10, padx=10)
        self.email.bind('<Return>', self.confirm_command)

        # Setting up phone field
        phone_label = customtkinter.CTkLabel(self.input_frame, text="Phone *:")
        phone_label.grid(row=9, column=0, pady=10, padx=10)
        self.phone = customtkinter.CTkEntry(
            self.input_frame,
            validate="key",
            validatecommand=(self.validate_input_cmd, '%P'),
            textvariable=phone, state=enable_entry)
        self.phone.grid(row=9, column=1, pady=10, padx=10)
        self.phone.bind('<Return>', self.confirm_command)


    def setup_modify_form(self):
        self.modify_mode = True
        self.setup_input_fields()

        confirm_label = "Update" if self.user else "Register"

        # Add confirm button
        register_button = customtkinter.CTkButton(self.input_frame, text=confirm_label, command=self.confirm_command)
        register_button.grid(row=10, column=1, padx=20, pady=20)

        # Add Cancel button
        register_button = customtkinter.CTkButton(self.input_frame, text="Cancel", command=self.cancel_command)
        register_button.grid(row=10, column=0, padx=20, pady=20)


    def setup_view_form(self):
        self.setup_input_fields()

        # Add edit button
        edit_button = customtkinter.CTkButton(self.input_frame, text="Edit", command=self.setup_modify_form)
        edit_button.grid(row=10, column=1, padx=20, pady=20)


    def clear_form(self):
        for child in self.input_frame.winfo_children():
            child.destroy()

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

    def update_user(self, event=None):
        """
        Updates the user's info using what is in the form

        Argument:
            event: Key press event for pressing enter
        """
        print("updating user")

    def cancel(self):
        """
        Return to the profile view page
        """
        self.modify_mode = False
        self.setup_inputs()