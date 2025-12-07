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

        self.input_frame = customtkinter.CTkFrame(self.parent)
        self.input_frame.pack()

        # Different search commands
        self.refresh_command = self.controller.refresh_table if self.for_expenses else self
        self.create_filter_section()

    def create_filter_section(self):
        """
        Displays the filter section for filtering the expenses table
        """
        # Setting up date field
        start_date_label = customtkinter.CTkLabel(self.input_frame, text="Start Date")
        start_date_label.grid(row=0, column=0)
        self.start_date = DateEntry(self.input_frame, selectmode='day', state='normal', showweeknumbers=False, **self.controller.controller.calendar_style)
        self.start_date.grid(row=1, column=0, padx=(0, 20))

        # Ensures that the DateEntry is at the top level to prevent clicking the fields behind it
        #self.start_date._top_cal.transient(self)
        self.start_date._top_cal.lift()
        
        end_date_label = customtkinter.CTkLabel(self.input_frame, text="End Date")
        end_date_label.grid(row=0, column=1)
        self.end_date = DateEntry(self.input_frame, selectmode='day', state='normal', showweeknumbers=False, **self.controller.controller.calendar_style)
        self.end_date.grid(row=1, column=1)

        # Have date range filters empty by default
        self.start_date.delete(0, customtkinter.END)
        self.end_date.delete(0, customtkinter.END)

        # Creating filters that are only meant for the expenses page:
        if self.for_expenses:
            # Category Filter
            category_label = customtkinter.CTkLabel(self.input_frame, text="Categories")
            category_label.grid(row=2, column=0)
            categories = ["--Category--"]
            for category in self.controller.categories.keys():
                categories.append(category)
            self.category_filter = customtkinter.CTkOptionMenu(self.input_frame, values=categories)
            self.category_filter.grid(row=3, column=0)

            # Payment Method Filter
            payment_method_label = customtkinter.CTkLabel(self.input_frame, text="Payment Methods")
            payment_method_label.grid(row=2, column=1)
            method_of_purchase = ["--Payment Method--"]
            for method in self.controller.payment_methods.keys():
                method_of_purchase.append(method)
            self.method_filter = customtkinter.CTkOptionMenu(self.input_frame, values=method_of_purchase)
            self.method_filter.grid(row=3, column=1, padx=10)

            # Generic search bar
            self.search_bar = customtkinter.CTkEntry(self.input_frame, placeholder_text = "Search")
            self.search_bar.grid(row=3, column=6)

            self.input_frame.columnconfigure(4, weight=0)

        # Search button
        search_button = customtkinter.CTkButton(self.input_frame, text="Search", command=self.refresh_command, width=100)
        search_button.grid(row=1, column=5, padx=10)

        # Reset button
        reset_button = customtkinter.CTkButton(self.input_frame, text="Reset", command=self.clear_filters, width=100)
        reset_button.grid(row=1, column=6)
        
        self.input_frame.pack()


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