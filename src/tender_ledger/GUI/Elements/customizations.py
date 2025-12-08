# Author - Daniel Dang
# Filename - customizations.py
# Purpose - Handles the appearance of the customization section from the Profile page

import customtkinter
from ...Backend.categories import get_categories_for_list
from ...Backend.payment_methods import get_payment_methods_for_list
from ..Elements.confirmation_popup import ConfirmationPopup
from ..Elements.add_popup import AddPopup
from ..Elements.pagination import Pagination
from tkinter import ttk

OPTIONS_PER_PAGE = 10

class Customizations(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the Customizations

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db
        
        # Store the full lists
        self.all_categories = []
        self.all_methods = []

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
        self.all_categories = get_categories_for_list(self.user_id, self.db)

        categories_frame = customtkinter.CTkFrame(self)
        categories_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Label
        label = customtkinter.CTkLabel(categories_frame, text="Categories", font=self.controller.font_label)
        label.grid(row=0, column=0, pady=20)

        # Add button
        add_button = customtkinter.CTkButton(categories_frame, text="Add", command=lambda: self.display_popup("Category"), width=100)
        add_button.grid(row=0, column=1, sticky="e", padx=(20, 0), pady=20)

        # Adding columns to table
        columns = ('name', 'edit', 'delete')
        self.category_table = ttk.Treeview(categories_frame, columns=columns, show='headings')

        # Add headers to columns
        self.category_table.heading('name', text='Category')
        self.category_table.heading('edit', text="Edit")
        self.category_table.heading('delete', text="Delete")

        # Control column width
        self.category_table.column('name', width=175)
        self.category_table.column('edit', width=75, anchor="center")
        self.category_table.column('delete', width=100, anchor="center")

        # Bind left click event
        self.category_table.bind("<Button-1>", lambda event: self.action_click(event, True))

        self.category_table.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Add pagination
        self.category_pagination = Pagination(
            categories_frame, 
            OPTIONS_PER_PAGE, 
            self.all_categories,
            self.refresh_category_table
        )
        self.category_pagination.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.category_pagination.create_pagination_options()

        # Populate table
        self.refresh_category_table()

    def refresh_category_table(self):
        """
        Refreshes the category table with paginated data
        """
        # Clear the table
        for row in self.category_table.get_children():
            self.category_table.delete(row)

        if not self.all_categories:
            return

        # Calculate pagination
        current_page = self.category_pagination.current_page
        start = OPTIONS_PER_PAGE * (current_page - 1) if current_page != 0 else 0
        end = min(start + OPTIONS_PER_PAGE, len(self.all_categories))

        # Add categories to table
        for i in range(start, end):
            category = self.all_categories[i]
            category_id = category[0]
            category_name = category[1]
            edit = "Edit" if category[2] else ""
            delete = "Delete" if category[2] else ""
            self.category_table.insert('', 'end', iid=category_id, values=(category_name, edit, delete))

    def setup_payment_methods(self):
        """
        Setup the Payment Methods list
        """
        self.all_methods = get_payment_methods_for_list(self.user_id, self.db)

        methods_frame = customtkinter.CTkFrame(self)
        methods_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Label
        label = customtkinter.CTkLabel(methods_frame, text="Payment Methods", font=self.controller.font_label)
        label.grid(row=0, column=0, pady=20)

        # Add button
        add_button = customtkinter.CTkButton(methods_frame, text="Add", command=lambda: self.display_popup("Payment Method"), width=100)
        add_button.grid(row=0, column=1, sticky="e", padx=(20, 0), pady=20)

        # Adding columns to table
        columns = ('name', 'edit', 'delete')
        self.method_table = ttk.Treeview(methods_frame, columns=columns, show='headings')

        # Add headers to columns
        self.method_table.heading('name', text='Payment Method')
        self.method_table.heading('edit', text="Edit")
        self.method_table.heading('delete', text="Delete")

        # Control column width
        self.method_table.column('name', width=175)
        self.method_table.column('edit', width=75, anchor="center")
        self.method_table.column('delete', width=100, anchor="center")

        # Bind left click event
        self.method_table.bind("<Button-1>", lambda event: self.action_click(event, False))

        self.method_table.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Add pagination
        self.method_pagination = Pagination(
            methods_frame, 
            OPTIONS_PER_PAGE, 
            self.all_methods,
            self.refresh_method_table
        )
        self.method_pagination.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.method_pagination.create_pagination_options()

        # Populate table
        self.refresh_method_table()

    def refresh_method_table(self):
        """
        Refreshes the payment method table with paginated data
        """
        # Clear the table
        for row in self.method_table.get_children():
            self.method_table.delete(row)

        if not self.all_methods:
            return

        # Calculate pagination
        current_page = self.method_pagination.current_page
        start = OPTIONS_PER_PAGE * (current_page - 1) if current_page != 0 else 0
        end = min(start + OPTIONS_PER_PAGE, len(self.all_methods))

        # Add methods to table
        for i in range(start, end):
            method = self.all_methods[i]
            method_id = method[0]
            method_name = method[1]
            edit = "Edit" if method[2] else ""
            delete = "Delete" if method[2] else ""
            self.method_table.insert('', 'end', iid=method_id, values=(method_name, edit, delete))

    def clear_form(self):
        """
        Clear the frame holding the user form
        """
        for child in self.winfo_children():
            child.destroy()

    def action_click(self, event, is_category):
        """
        Handles on click events for the table. User should be clicking on the values in the 
        Action column for this to work. Edit and delete functionality will depend on which half
        of the cell the user clicks on

        Arguments:
            event: Key press event for clicking the mouse
            is_category (bool): True if the table is for categories
                                False if the table is for payment methods
        """
        # Assign variables depending on type of table
        table = self.category_table if is_category else self.method_table
        popup_type = "Category" if is_category else "Payment Method"

        # Get coordinates of event click
        x = event.x
        y = event.y

        # Get region of event and return if not a cell
        region = table.identify_region(x, y)
        if region != "cell": 
            return

        # Get column
        col_index = table.identify_column(x)
        col = table.column(col_index)

        if col["id"] == "edit" or col["id"] == "delete":
            id = int(table.identify_row(y))

            # Return if the cell is not 'Edit' or 'Delete'
            cell_value = table.set(id, col["id"])
            if not cell_value or cell_value.strip() == "":
                return

            if col["id"] == "edit":
                self.display_popup(popup_type, editing=id)
            else:
                # Display confirmation popup before deleting
                deleting = (popup_type, id, self)
                self.display_popup(popup_type, deleting=deleting)

    def display_popup(self, action, deleting=None, editing=None):
        """
        Displays the popup for adding or deleting expenses

        Argument:
            action (String): Could be either 'Category' or 'Payment Method'
            deleting (tuple): First element contains type being deleted, second contains ID
            editing (int): Contains ID of expense to edit
        """
        if not deleting and not editing:
            popup = AddPopup(self, self.controller, self.db, action)
        elif editing:
            popup = AddPopup(self, self.controller, self.db, action, editing=editing)
        else:
            popup = ConfirmationPopup(parent=self, controller=self.controller, db=self.db, action=deleting)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)