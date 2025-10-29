# Author - Daniel Dang
# Filename - dashboard_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter

class DashboardPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        """
        Initializes a new instance of the DashboardPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
        """
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="Dashboard")
        label.pack()



    