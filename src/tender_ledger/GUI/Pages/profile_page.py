# Author - Daniel Dang
# Filename - profile_page.py
# Purpose - Handles the appearance of the profile page

import customtkinter
from ...Backend.users import get_user_by_id
from ..Elements.user_form import UserForm
from ..Elements.customizations import Customizations

class ProfilePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ProfilePage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        label = customtkinter.CTkLabel(self, text="My Profile (CURRENTLY DEVELOPING)", font=self.controller.font_label)
        label.grid(row=0, column=0)

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew")

        self.tabview.add("Profile")
        self.tabview.add("Customization")

        self.page_frame = customtkinter.CTkFrame(self.tabview.tab("Profile"))
        self.page_frame.grid(row=0, column=0)

        self.customization_frame = customtkinter.CTkFrame(self.tabview.tab("Customization"))
        self.customization_frame.grid(row=0, column=0)

        self.user_form = UserForm(self.page_frame, self, self.db, None, None, False)
        self.user_form.pack()

        self.customizations = Customizations(self.customization_frame, self, self.db)
        self.customizations.pack()

        self.tabview._segmented_button.configure(command=self.on_tab_changed)

    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id
        got_user = get_user_by_id(user_id, self.db)
        
        user = {
            "user_id" : got_user[0][0],
            "username" : got_user[0][1],
            "first_name" : got_user[0][3],
            "last_name" : got_user[0][4],
            "birthday" : got_user[0][5],
            "email" : got_user[0][6],
            "phone" : got_user[0][7]
        }
        self.user_form.set_user(user)

        # Set Profile tab to be default tab
        self.tabview.set("Profile")

    def on_tab_changed(self, event):
        if event == "Customization":
            self.page_frame.grid_forget()
            self.customization_frame.grid(row=0, column=0)

            self.customizations.set_user(self.user_id)
            
        if event == "Profile":
            self.customization_frame.grid_forget()
            self.page_frame.grid(row=0, column=0)

            self.refresh_page(self.user_id)
        

