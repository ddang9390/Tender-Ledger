# Author - Daniel Dang
# Filename - error_message.py
# Purpose - Handles the appearance of the customization section from the Profile page

import customtkinter
from ...Backend.categories import get_categories_for_list
from ...Backend.payment_methods import get_payment_methods_for_list
from ..Elements.confirmation_popup import ConfirmationPopup
from ..Elements.add_popup import AddPopup
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
        self.parent = parent
        self.controller = controller
        self.db = db

    def set_user(self, user_id):
        """
        Fill in the fields using the user's info

        Argument:
            user_id (int): The user's ID
        """
        self.user_id = user_id
        self.refresh()


    def refresh(self):
        """
        Refreshes the Customizations tab
        """
        self.clear_form()

        self.setup_categories()
        self.setup_payment_methods()


    def setup_categories(self):
        """
        Setup the Categories list
        """
        categories = get_categories_for_list(self.user_id, self.db)

        categories_frame = customtkinter.CTkFrame(self)
        categories_frame.grid(row=0, column=0, sticky="nsew")

        # Label
        label = customtkinter.CTkLabel(categories_frame, text="Categories")
        label.grid(row=0, column=0)

        # Add button
        add_button = customtkinter.CTkButton(categories_frame, text="Add", command=lambda: self.display_popup("Category"))
        add_button.grid(row=0, column=1, sticky="e")

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

        # Bind left click event
        self.category_table.bind("<Button-1>", self.category_action_click)

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

        # Add button
        add_button = customtkinter.CTkButton(methods_frame, text="Add", command=lambda: self.display_popup("Payment Method"))
        add_button.grid(row=0, column=1, sticky="e")

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

        # Bind left click event
        self.method_table.bind("<Button-1>", self.method_action_click)

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


    # TODO - REFACTOR THIS - IT'S A COPIED AND PASTED FUNCTION
    # TODO - affects rows without edit and delete text as well
    def category_action_click(self, event):
        """
        Handles on click events for the table. User should be clicking on the values in the 
        Action column for this to work. Edit and delete functionality will depend on which half
        of the cell the user clicks on
        """
        # Get coordinates of event click
        x = event.x
        y = event.y

        # Get region of event and return if not a cell
        region = self.category_table.identify_region(x, y)
        if region != "cell": return

        # Get column
        col_index = self.category_table.identify_column(x)
        col = self.category_table.column(col_index)

        if col["id"] == "edit" or col["id"] == "delete":
            # Get expense id
            category_id = int(self.category_table.identify_row(y))

            if col["id"] == "edit":
                self.display_popup("Category", editing=category_id)
            else:
                # Display confirmation popup before deleting expense
                deleting = ("Category", category_id, self)
                self.display_popup("Category",deleting=deleting)

    def method_action_click(self, event):
        """
        Handles on click events for the table. User should be clicking on the values in the 
        Action column for this to work. Edit and delete functionality will depend on which half
        of the cell the user clicks on
        """
        # Get coordinates of event click
        x = event.x
        y = event.y

        # Get region of event and return if not a cell
        region = self.method_table.identify_region(x, y)
        if region != "cell": return

        # Get column
        col_index = self.method_table.identify_column(x)
        col = self.method_table.column(col_index)

        if col["id"] == "edit" or col["id"] == "delete":
            # Get expense id
            method_id = int(self.method_table.identify_row(y))

            if col["id"] == "edit":
                self.display_popup("Payment Method", editing=method_id)
            else:
                # Display confirmation popup before deleting expense
                deleting = ("Payment Method", method_id, self)
                self.display_popup("Payment Method", deleting=deleting)

    def display_popup(self, action, deleting=None, editing=None):
        """
        Displays the popup for adding or deleting expenses

        Argument:
            action (String): Could be either 'Category' or 'Payment Method'
            deleting (tuple): First element contains type being deleted, second contains ID
            editing (int): Contains ID of expense to edit
        """
        # TODO - need scrollbars
        if not deleting and not editing:
            popup = AddPopup(self, self.controller, self.db, action)

        elif editing:
            popup = AddPopup(self, self.controller, self.db, action, editing=editing)

        else:
            popup = ConfirmationPopup(parent=self, controller=self.controller,db=self.db, action=deleting)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)