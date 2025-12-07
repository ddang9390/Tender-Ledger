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

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = customtkinter.CTkLabel(self, text="My Profile", font=self.controller.font_label)
        label.grid(row=0, column=0)

        # Creating tab menu
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew")

        # Adding tabs
        self.tabview.add("Profile")
        self.tabview.add("Customization")

        # Customizing Tabs
        self.profile_tab = customtkinter.CTkFrame(
            self.tabview.tab("Profile"), 
            border_width=2, 
            border_color="gray",
            corner_radius=10
        )
        self.profile_tab.grid(row=1, column=1, sticky="nsew")

        self.customizations_tab = customtkinter.CTkFrame(
            self.tabview.tab("Customization"), 
            border_width=2, 
            border_color="gray",
            corner_radius=10
        )
        self.customizations_tab.grid(row=1, column=1, sticky="nsew")
        self.create_spacers()

        # User tab
        self.user_form = UserForm(self.profile_tab, self.controller, self.db, None, None, False)
        self.user_form.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        # Customization tab
        self.customizations = Customizations(self.customizations_tab, self.controller, self.db)
        self.customizations.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.tabview._segmented_button.configure(command=self.on_tab_changed)

    def create_spacers(self):
        """
        Creating spacers to center the contents of the tabs
        """
        # For the Profile tab
        self.tabview.tab("Profile").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Profile").grid_rowconfigure(1, weight=0)
        self.tabview.tab("Profile").grid_rowconfigure(2, weight=1)
        
        self.tabview.tab("Profile").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Profile").grid_columnconfigure(1, weight=0)
        self.tabview.tab("Profile").grid_columnconfigure(2, weight=1) 

        # For the Customization tab
        self.tabview.tab("Customization").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Customization").grid_rowconfigure(1, weight=0)
        self.tabview.tab("Customization").grid_rowconfigure(2, weight=1)
        
        self.tabview.tab("Customization").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Customization").grid_columnconfigure(1, weight=0)
        self.tabview.tab("Customization").grid_columnconfigure(2, weight=1) 

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
        """
        Handles the behavior of the TabView when the tabs are clicked on

        Argument:
            event (string): The name of the tab that was clicked on
        """
        if event == "Customization":
            self.customizations.set_user(self.user_id)
            self.tabview.set("Customization")
            
        if event == "Profile":
            self.refresh_page(self.user_id)

    
        

