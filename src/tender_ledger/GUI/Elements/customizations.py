# Author - Daniel Dang
# Filename - error_message.py
# Purpose - Handles the appearance of the customization section from the Profile page

import customtkinter
from ...Backend.categories import get_categories_for_list
from ...Backend.payment_methods import get_payment_methods_for_list
from tkinter import ttk

class Customizations(customtkinter.CTkFrame):
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

    def set_user(self, user_id):
        """
        Fill in the fields using the user's info

        Argument:
            user_id (int): The user's ID
        """
        self.clear_form()
        self.user_id = user_id

        self.setup_categories()
        self.setup_payment_methods()


    def setup_categories(self):
        """
        Setup the Categories list
        """
        categories = get_categories_for_list(self.user_id, self.db)

        categories_frame = customtkinter.CTkFrame(self)
        categories_frame.grid(row=0, column=0, sticky="nsew")


        label = customtkinter.CTkLabel(categories_frame, text="Categories")
        label.grid(row=0, column=0)

        # Adding columns to table
        columns = ('name', 'edit', 'delete')
        self.category_table = ttk.Treeview(categories_frame, columns=columns, show='headings')

        # Add headers to columns
        self.category_table.heading('name', text='Category')
        self.category_table.heading('edit', text="Edit")
        self.category_table.heading('delete', text="Delete")

        # Control column width
        self.category_table.column('name', width=150)
        self.category_table.column('edit', width=50, anchor="center")
        self.category_table.column('delete', width=50, anchor="center")

        # Add categories to list
        if categories:
            for category in categories:
                category_id = category[0]
                category_name = category[1]
                edit = ""
                delete = ""
                if category[2]:
                    edit = "Edit"
                    delete = "Delete"
                self.category_table.insert('', 'end', iid=category_id, values=(category_name, edit, delete))


        self.category_table.grid(row=1, column=0, sticky="nsew")

    def setup_payment_methods(self):
        """
        Setup the Payment Methods list
        """
        methods = get_payment_methods_for_list(self.user_id, self.db)

        methods_frame = customtkinter.CTkFrame(self)
        methods_frame.grid(row=0, column=1, sticky="nsew")


        label = customtkinter.CTkLabel(methods_frame, text="Payment Methods")
        label.grid(row=0, column=0)

        # Adding columns to table
        columns = ('name', 'edit', 'delete')
        self.method_table = ttk.Treeview(methods_frame, columns=columns, show='headings')

        # Add headers to columns
        self.method_table.heading('name', text='Payment Method')
        self.method_table.heading('edit', text="Edit")
        self.method_table.heading('delete', text="Delete")

        # Control column width
        self.method_table.column('name', width=150)
        self.method_table.column('edit', width=50, anchor="center")
        self.method_table.column('delete', width=50, anchor="center")

        # Add methods to list
        if methods:
            for method in methods:
                method_id = method[0]
                method_name = method[1]
                edit = ""
                delete = ""
                if method[2]:
                    edit = "Edit"
                    delete = "Delete"
                self.method_table.insert('', 'end', iid=method_id, values=(method_name, edit, delete))
        self.method_table.grid(row=1, column=0)
        

    def clear_form(self):
        """
        Clear the frame holding the user form
        """
        for child in self.winfo_children():
            child.destroy()