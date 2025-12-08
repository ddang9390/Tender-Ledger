# Author - Daniel Dang
# Filename - pagination.py
# Purpose - Handles the pagination component for tables

import customtkinter

class Pagination(customtkinter.CTkFrame):
    def __init__(self, parent, options_per_page, items, on_page_change=None):
        """
        Initializes a new instance of the Expense Table

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            options_per_page(int): The number of options to show per page
            items (list): A list of items that will populate the table
            on_page_change: Command to call when pagination button is pressed
        """
        super().__init__(parent)
        self.options_per_page = options_per_page

        self.items = items
        self.on_page_change = on_page_change

        self.pagination_frame = customtkinter.CTkFrame(self)
        self.pagination_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.current_page = 1

    def create_pagination_options(self, items=None):
        """
        Displays pagination options for the expenses table

        Argument:
            items (list): A list of items that will populate the table
        """
        if items:
            self.items = items
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

    def calculate_total_pages(self):
        """
        Calculate the total number of pages in the table
        """
        self.total_pages = len(self.items) // self.options_per_page
        if len(self.items) % self.options_per_page != 0:
            self.total_pages += 1

    def go_to_prev_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page -= 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        self.update_pagination_buttons()
        self.on_page_change()

    def go_to_next_page(self):
        """
        Go to the previous page in the table
        """
        self.current_page += 1
        self.page_label.configure(text=f"{self.current_page}/{self.total_pages}")

        # Enable or disable buttons
        self.update_pagination_buttons()
        self.on_page_change()

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

    