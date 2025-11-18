# Author - Daniel Dang
# Filename - login.py
# Purpose - Handles the appearance and logic of the password field

import customtkinter

class PasswordField(customtkinter.CTkFrame):
    def __init__(self, parent, command):
        """
        Initializes a new instance of the LoginPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            command: The function that should be called when pressing 'Enter'
        """
        super().__init__(parent)
        self.parent = parent
        self.command = command

        self.setup_field()

        self.showing = False

    def setup_field(self):
        """
        Setup the password field and the toggle button
        """
        self.password = customtkinter.CTkEntry(self, show="*")
        self.password.grid(row=0, column=0)
        self.password.bind('<Return>', self.command)

        # TODO - replace text with show/hide image
        self.password_reveal = customtkinter.CTkButton(self, text="Show Password", command=self.show_hide_password)
        self.password_reveal.grid(row=0, column=1)

    def show_hide_password(self):
        """
        Shows or hides the password field
        """
        if not self.showing:
            self.password.configure(show="")
            self.password_reveal.configure(text="Hide Password")
            self.showing = True
        else:
            self.password.configure(show="*")
            self.password_reveal.configure(text="Show Password")
            self.showing = False

    def get(self):
        """
        Gets what is in the password field

        Returns:
            str: What is in the password field 
        """
        return self.password.get()