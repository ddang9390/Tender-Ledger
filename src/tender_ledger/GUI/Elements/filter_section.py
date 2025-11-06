# Author - Daniel Dang
# Filename - filter_section.py
# Purpose - Handles the appearance and fucntion of the filter section

import customtkinter

class FilterSection:
    def __init__(self, parent, controller, for_expenses=False):
        """
        Initializes a new instance of the filter section

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller: The page that acts as a controller
            for_expenses (bool): True if the filter section is for the Expenses page.
                                 False if not
        """
        self.parent = parent
        self.controller = controller
        self.for_expenses = for_expenses

        self.create_filter_section()
        

    def create_filter_section(self):
        """
        Displays the filter section for filtering the expenses table
        """
        # TODO - date range filter

        # Creating filters that are only meant for the expenses page:
        if self.for_expenses:
            # Generic search bar
            self.search_bar = customtkinter.CTkEntry(self.parent, placeholder_text = "Search")
            self.search_bar.pack(side="left")

            # Category Filter
            categories = ["--Category--"]
            for category in self.controller.categories.keys():
                categories.append(category)
            self.category_filter = customtkinter.CTkOptionMenu(self.parent, values=categories)
            self.category_filter.pack(side="left")

            # Payment Method Filter
            method_of_purchase = ["--Payment Method--"]
            for method in self.controller.payment_methods.keys():
                method_of_purchase.append(method)
            self.method_filter = customtkinter.CTkOptionMenu(self.parent, values=method_of_purchase)
            self.method_filter.pack(side="left", padx=10)

        # Search button
        search_button = customtkinter.CTkButton(self.parent, text="Search", command=self.controller.refresh_table)
        search_button.pack(side="right")

        # Reset button
        reset_button = customtkinter.CTkButton(self.parent, text="Reset", command=self.clear_filters)
        reset_button.pack(side="right")
        
    def clear_filters(self):
        """
        Clear the filters in the filter section
        """
        # TODO - include date range stuff here

        if self.for_expenses:
            clear = customtkinter.StringVar(value="")
            self.search_bar.configure(textvariable=clear)

            self.category_filter.set("--Category--")
            self.method_filter.set("--Payment Method--")

            self.controller.refresh_table()