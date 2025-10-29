# Author - Daniel Dang
# Filename - profile_page.py
# Purpose - Handles the appearance of the profile page

import customtkinter

class ProfilePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        """
        Initializes a new instance of the ProfilePage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
        """
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="My Profile")
        label.pack()

