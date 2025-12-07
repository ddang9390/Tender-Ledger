# Author - Daniel Dang
# Filename - filter_section.py
# Purpose - Handles the appearance and fucntion of the filter section

import customtkinter
from tkcalendar import DateEntry

class FilterSection:
    def __init__(self, parent, controller, for_expenses=False):
        """
        Initializes a new instance of the filter section

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller: The page that acts as a controller
            for_expenses (bool): True if the filter section is for the Expenses page.
                                 False if not
        """
        self.parent = parent
        self.controller = controller
        self.for_expenses = for_expenses

        self.input_frame = customtkinter.CTkFrame(self.parent, fg_color="transparent")
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.input_frame.rowconfigure(0, weight=0)
        self.input_frame.rowconfigure(1, weight=0)

        # Different search commands
        self.refresh_command = self.controller.refresh_table if self.for_expenses else self.controller.filter_page
        self.create_filter_section()

    def create_filter_section(self):
        """
        Displays the filter section for filtering the expenses table
        """
        # Configure columns
        self.input_frame.columnconfigure(0, weight=0)
        self.input_frame.columnconfigure(1, weight=0)
        self.input_frame.columnconfigure(2, weight=1)
        self.input_frame.columnconfigure(3, weight=0)
        self.input_frame.columnconfigure(4, weight=0)

        # Setting up date field
        start_date_label = customtkinter.CTkLabel(self.input_frame, text="Start Date")
        start_date_label.grid(row=0, column=0, sticky="w")
        self.start_date = DateEntry(self.input_frame, selectmode='day', state='normal', showweeknumbers=False, **self.controller.controller.calendar_style)
        self.start_date.grid(row=1, column=0, padx=(0, 20), sticky="w")

        # Ensures that the DateEntry is at the top level to prevent clicking the fields behind it
        self.start_date._top_cal.lift()
        
        end_date_label = customtkinter.CTkLabel(self.input_frame, text="End Date")
        end_date_label.grid(row=0, column=1, padx=10, sticky="w")
        self.end_date = DateEntry(self.input_frame, selectmode='day', state='normal', showweeknumbers=False, **self.controller.controller.calendar_style)
        self.end_date.grid(row=1, column=1, padx=10, sticky="w")

        # Have date range filters empty by default
        self.start_date.delete(0, customtkinter.END)
        self.end_date.delete(0, customtkinter.END)

        current_col = 2

        # Creating filters that are only meant for the expenses page:
        if self.for_expenses:
            # Category Filter
            category_label = customtkinter.CTkLabel(self.input_frame, text="Categories")
            category_label.grid(row=2, column=0, sticky="w")
            categories = ["--Category--"]
            for category in self.controller.categories.keys():
                categories.append(category)
            self.category_filter = customtkinter.CTkOptionMenu(self.input_frame, values=categories)
            self.category_filter.grid(row=3, column=0, sticky="w")

            # Payment Method Filter
            payment_method_label = customtkinter.CTkLabel(self.input_frame, text="Payment Methods")
            payment_method_label.grid(row=2, column=1, padx=10, sticky="w")
            method_of_purchase = ["--Payment Method--"]
            for method in self.controller.payment_methods.keys():
                method_of_purchase.append(method)
            self.method_filter = customtkinter.CTkOptionMenu(self.input_frame, values=method_of_purchase)
            self.method_filter.grid(row=3, column=1, padx=10, sticky="w")

            # Generic search bar
            self.search_bar = customtkinter.CTkEntry(self.input_frame, placeholder_text = "Search")
            self.search_bar.grid(row=3, column=3, columnspan=2, sticky="ew")

            current_col = 3

        # Search button
        search_button = customtkinter.CTkButton(self.input_frame, text="Search", command=self.refresh_command, width=100)
        search_button.grid(row=1, column=3, padx=(0, 10), sticky="e")

        # Reset button
        reset_button = customtkinter.CTkButton(self.input_frame, text="Reset", command=self.clear_filters, width=100)
        reset_button.grid(row=1, column=4, sticky="e")
        
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


    def clear_filters(self):
        """
        Clear the filters in the filter section
        """
        # Clear date fields
        self.start_date.delete(0, customtkinter.END)
        self.end_date.delete(0, customtkinter.END)

        if self.for_expenses:
            clear = customtkinter.StringVar(value="")
            self.search_bar.configure(textvariable=clear)

            self.category_filter.set("--Category--")
            self.method_filter.set("--Payment Method--")

            self.controller.refresh_table()