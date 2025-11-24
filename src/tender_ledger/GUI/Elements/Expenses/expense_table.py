# Author - Daniel Dang
# Filename - expense_table.py
# Purpose - Handles the appearance and functionality of the expenses table

import customtkinter
from ....Backend.expenses import get_expenses_for_user
from tkinter import ttk

class ExpenseTable():
    def __init__(self, parent, controller, filter_section, db):
        """
        Initializes a new instance of the Expense Table

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (ExpensesPage): The expenses page that acts as a controller
            filter_section (FilterSection): The filter section that will modify the table
            db (DatabaseManager): Instance of database manager being used
        """
        self.parent = parent
        self.controller = controller
        self.filter_section = filter_section
        self.user_id = self.controller.user_id
        self.db = db

        self.expenses = get_expenses_for_user(self.user_id, self.db)

        # Setting page options
        self.current_page = 1
        self.options_per_page = 10

        # Creating table and pagination options
        self.create_table()
        self.create_pagination_options()
        self.refresh_table()

    def create_table(self):
        """
        Displays the table for the user's expenses
        """
        self.expense_table_frame = customtkinter.CTkFrame(self.parent) 
        self.expense_table_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

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
                self.controller.display_popup(editing=expense_id)
            else:
                # Display confirmation popup before deleting expense
                deleting = ("Expense", expense_id, self)
                self.controller.display_popup(deleting)


    def refresh_table(self):
        """
        Refreshes the table by clearing it and then repopulating it
        """
        # Get date values
        start_date = self.filter_section.start_date.get()
        # Ensure date fields are not empty
        if start_date:
            start_date = self.filter_section.start_date.get_date()
        end_date = self.filter_section.end_date.get()
        if end_date:
            end_date = self.filter_section.end_date.get_date()

        search = self.filter_section.search_bar.get()
        category_search = self.controller.categories[self.filter_section.category_filter.get()] if self.filter_section.category_filter.get() != "--Category--" else None
        payment_method_search = self.controller.payment_methods[self.filter_section.method_filter.get()] if self.filter_section.method_filter.get() != "--Payment Method--" else None


        self.expenses = get_expenses_for_user(self.user_id, self.db, category=category_search, payment_method=payment_method_search, search=search, start_date=start_date, end_date=end_date)

        # Clear the table
        for row in self.expense_table.get_children():
            self.expense_table.delete(row)

        # Calculate start and end indices for pagination
        if self.current_page != 0:
            start = self.options_per_page * (self.current_page-1)
        else:
            start = 0
        end = start + self.options_per_page
        if end > len(self.expenses):
            end = len(self.expenses)

        # Add expenses to the table
        if len(self.expenses) > 0: 
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

        # Refresh pagination options
        self.create_pagination_options()
        if self.current_page > self.total_pages:
            self.go_to_prev_page()

    def create_pagination_options(self):
        """
        Displays pagination options for the expenses table
        """
        self.pagination_frame = customtkinter.CTkFrame(self.parent)
        self.pagination_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.calculate_total_pages()

        # Previous button
        self.prev_button = customtkinter.CTkButton(self.pagination_frame, text="Prev", command=self.go_to_prev_page)
        self.prev_button.grid(row=0, column=0)

        # Page label
        self.page_label = customtkinter.CTkLabel(self.pagination_frame, text=f"{self.current_page}/{self.total_pages}")
        self.page_label.grid(row=0, column=1, padx=10)

        # Next button
        self.next_button = customtkinter.CTkButton(self.pagination_frame, text="Next", command=self.go_to_next_page)
        self.next_button.grid(row=0, column=2)

        # Update status of pagination buttons
        self.update_pagination_buttons()


    def go_to_prev_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page -= 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        self.update_pagination_buttons()
        self.refresh_table()

    def go_to_next_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page += 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        self.update_pagination_buttons()
        self.refresh_table()

    def update_pagination_buttons(self):
        """
        Disables or enables the pagination buttons depending on what page the user is on
        """
        self.calculate_total_pages()

        # If at the beginning, disable prev button and ensure next button is enabled
        if self.current_page == 1 or self.current_page == 0:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")  

        # If at the end, disable next button and ensure prev button is enabled
        if self.current_page == self.total_pages:
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")

    def calculate_total_pages(self):
        """
        Calculate the total number of pages in the table
        """
        self.total_pages = len(self.expenses) // self.options_per_page
        if len(self.expenses) % self.options_per_page != 0:
            self.total_pages += 1