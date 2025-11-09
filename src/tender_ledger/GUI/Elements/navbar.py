# Author - Daniel Dang
# Filename - navbar.py
# Purpose - Handles the appearance and logic of the navbar

import customtkinter

class NavBar(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the Navbar

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        label = customtkinter.CTkLabel(self, text="Navbar", font=self.controller.font_label)
        label.grid(row=0, column=0, padx=20, pady=20)

        expenses_button = customtkinter.CTkButton(self, text="Expenses", command=lambda: controller.show_page("ExpensesPage"))
        expenses_button.grid(row=1, column=0, padx=20, pady=20)

        dashboard_button = customtkinter.CTkButton(self, text="Dashboard", command=lambda: controller.show_page("DashboardPage"))
        dashboard_button.grid(row=2, column=0, padx=20, pady=20)

        profile_button = customtkinter.CTkButton(self, text="My Profile", command=lambda: controller.show_page("ProfilePage"))
        profile_button.grid(row=3, column=0, padx=20, pady=20)

        #TODO - add logout button for returning to login page
        logout_button = customtkinter.CTkButton(self, text="Logout", command=self.logout)
        logout_button.grid(row=4, column=0, sticky="s")

    def logout(self):
        """
        Log the user out and send them to the login page
        """
        self.controller.user_id = None
        self.controller.show_page("LoginPage")
        
