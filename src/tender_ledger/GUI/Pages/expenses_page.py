# Author - Daniel Dang
# Filename - expenses_page.py
# Purpose - Handles the appearance of the expenses page

import customtkinter
import re
from ..Elements.add_expense_popup import AddExpensePopup
from ..Elements.confirmation_popup import ConfirmationPopup
from ...Backend.categories import get_categories_for_user
from ...Backend.payment_methods import get_payment_methods_for_user
from ...Backend.expenses import get_expenses_for_user
from tkinter import ttk

class ExpensesPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ExpensesPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db = db

        #TODO - change user id once login functionality is implemented
        self.user_id = -1
        self.categories = get_categories_for_user(self.user_id, self.db)
        self.payment_methods = get_payment_methods_for_user(self.user_id, self.db)
        self.expenses = get_expenses_for_user(self.user_id, self.db)
        
        # Creating header section
        label = customtkinter.CTkLabel(self, text="My Expenses")
        label.grid(row=0, column=0, sticky="w")

        add_button = customtkinter.CTkButton(self, text="Add", command=self.display_popup)
        add_button.grid(row=0, column=1, sticky="e")

        # Creating filter section
        self.filter_frame = customtkinter.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky="nsew")
        self.create_filter_section()

        #--------Table Stuff--------#
        # TODO - move table related stuff into new file, this is getting too much
        # Pagination controls
        self.current_page = 1
        self.options_per_page = 5
        self.total_pages = len(self.expenses) // self.options_per_page
        if len(self.expenses) % self.options_per_page != 0:
            self.total_pages += 1

        # Creating table section
        self.create_table()
        self.refresh_table()
        self.expense_table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.create_pagination_options()
        # ---------------------------#

    def display_popup(self, deleting=None, editing=None):
        """
        Displays the popup for adding or deleting expenses

        Argument:
            deleting (tuple): First element contains type being deleted, second contains ID
            editing (int): Contains ID of expense to edit
        """
        if not deleting and not editing:
            popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=self.categories, payment_methods=self.payment_methods, expense_page=self, db=self.db)
        
        elif editing:
            popup = AddExpensePopup(parent=self.parent, controller=self.controller, categories=self.categories, payment_methods=self.payment_methods, expense_page=self, db=self.db, editing=editing)
        else:
            popup = ConfirmationPopup(parent=self.parent, controller=self.controller,db=self.db, action=deleting)

        # Ensures that the popup is updated and visible before grabbing it
        popup.update_idletasks()
        popup.deiconify()

        # Display the popup
        popup.grab_set()
        popup.wait_window(popup)

    def create_filter_section(self):
        """
        Displays the filter section for filtering the expenses table
        """
        # Generic search bar
        self.search_bar = customtkinter.CTkEntry(self.filter_frame, placeholder_text = "Search")
        self.search_bar.pack(side="left")

        # Category Filter
        categories = ["--Category--"]
        for category in self.categories.keys():
            categories.append(category)
        self.category_filter = customtkinter.CTkOptionMenu(self.filter_frame, values=categories)
        self.category_filter.pack(side="left")

        # Payment Method Filter
        method_of_purchase = ["--Payment Method--"]
        for method in self.payment_methods.keys():
            method_of_purchase.append(method)
        self.method_filter = customtkinter.CTkOptionMenu(self.filter_frame, values=method_of_purchase)
        self.method_filter.pack(side="left", padx=10)

        # Search button
        search_button = customtkinter.CTkButton(self.filter_frame, text="Search", command=self.refresh_table)
        search_button.pack(side="right")

        # Reset button
        reset_button = customtkinter.CTkButton(self.filter_frame, text="Reset", command=self.clear_filters)
        reset_button.pack(side="right")
        
    def clear_filters(self):
        """
        Clear the filters in the filter section
        """
        clear = customtkinter.StringVar(value="")
        self.search_bar.configure(textvariable=clear)

        self.category_filter.set("--Category--")
        self.method_filter.set("--Payment Method--")

    #--------Table Stuff--------#
    def create_pagination_options(self):
        """
        Displays pagination options for the expenses table
        """
        self.pagination_frame = customtkinter.CTkFrame(self)
        self.pagination_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # Previous button
        self.prev_button = customtkinter.CTkButton(self.pagination_frame, text="Prev", command=self.go_to_prev_page)
        self.prev_button.grid(row=0, column=0)

        # Page label
        self.page_label = customtkinter.CTkLabel(self.pagination_frame, text=f"{self.current_page}/{self.total_pages}")
        self.page_label.grid(row=0, column=1, padx=10)

        # Next button
        self.next_button = customtkinter.CTkButton(self.pagination_frame, text="Next", command=self.go_to_next_page)
        self.next_button.grid(row=0, column=2)

        # Previous button is disabled by default
        self.prev_button.configure(state="disabled")

        # Disable next button if only one page is available
        if self.current_page == self.total_pages:
            self.next_button.configure(state="disabled")


    def go_to_prev_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page -= 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        if self.current_page == 1:
            self.prev_button.configure(state="disabled")
        if self.current_page != self.total_pages:
            self.next_button.configure(state="normal")

        self.refresh_table()

    def go_to_next_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page += 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        if self.current_page == self.total_pages:
            self.next_button.configure(state="disabled")
        if self.current_page != 1:
            self.prev_button.configure(state="normal")

        self.refresh_table()

    def create_table(self):
        """
        Displays the table for the user's expenses
        """
        self.expense_table_frame = customtkinter.CTkFrame(self) 

        # Adding columns to table
        columns = ('date', 'amount', 'category', 'payment method', 'location', 'edit', 'delete')
        self.expense_table = ttk.Treeview(self.expense_table_frame, columns=columns, show='headings')

        # Add headers to columns
        self.expense_table.heading('date', text='Date')
        self.expense_table.heading('amount', text='Amount')
        self.expense_table.heading('category', text='Category')
        self.expense_table.heading('payment method', text='Payment Method')
        self.expense_table.heading('location', text='Location')
        self.expense_table.heading('edit', text="Edit")
        self.expense_table.heading('delete', text="Delete")

        # Control column width
        self.expense_table.column('date', width=100)
        self.expense_table.column('amount', width=100)
        self.expense_table.column('category', width=100)
        self.expense_table.column('payment method', width=150)
        self.expense_table.column('location', width=200)
        self.expense_table.column('edit', width=75, anchor="center")
        self.expense_table.column('delete', width=100, anchor="center")
        self.expense_table.grid(row=0, column=0, sticky="nsew")

        # Bind left click event
        self.expense_table.bind("<Button-1>", self.action_click)

    def action_click(self, event):
        """
        Handles on click events for the table. User should be clicking on the values in the 
        Action column for this to work. Edit and delete functionality will depend on which half
        of the cell the user clicks on
        """
        # Get coordinates of event click
        x = event.x
        y = event.y

        # Get region of event and return if not a cell
        region = self.expense_table.identify_region(x, y)
        if region != "cell": return

        # Get column
        col_index = self.expense_table.identify_column(x)
        col = self.expense_table.column(col_index)

        if col["id"] == "edit" or col["id"] == "delete":
            # Get expense id
            expense_id = int(self.expense_table.identify_row(y))

            if col["id"] == "edit":
                self.display_popup(editing=expense_id)
            else:
                # Display confirmation popup before deleting expense
                deleting = ("Expense", expense_id, self)
                self.display_popup(deleting)


    def refresh_table(self):
        """
        Refreshes the table by clearing it and then repopulating it
        """
        # Get values from filter section
        search = self.search_bar.get()
        category_search = self.categories[self.category_filter.get()] if self.category_filter.get() != "--Category--" else None
        payment_method_search = self.payment_methods[self.method_filter.get()] if self.method_filter.get() != "--Payment Method--" else None

        self.expenses = get_expenses_for_user(self.user_id, self.db, category=category_search, payment_method=payment_method_search, search=search)

        # Clear the table
        for row in self.expense_table.get_children():
            self.expense_table.delete(row)

        # Calculate start and end indices for pagination
        start = self.options_per_page * (self.current_page-1)
        end = start + self.options_per_page
        if end > len(self.expenses):
            end = len(self.expenses)

        # Add expenses to the table
        for i in range(start, end):
            expense = self.expenses[i]
            date = expense[1]
            amount = f"${expense[0]:.2f}"
            category = expense[3]
            payment_method = expense[2]
            location = expense[4]

            # Use item identifier of Treeview, makes getting expense ID easier
            expense_id = expense[-1]

            display_values = (date, amount, category, payment_method, location, "Edit", "Delete")
            self.expense_table.insert('', 'end', values=display_values, iid=expense_id)
