# Author - Daniel Dang
# Filename - error_message.py
# Purpose - Handles the appearance of the error message

import customtkinter

class ErrorMessage():
    def __init__(self, parent, controller):
        """
        Initializes an instance of the error message

        Arguments:
            parent: The page that the popup will show in
            controller: The parent's controller
        """
        self.parent = parent
        self.controller = controller
        self.font_label = customtkinter.CTkFont(family="Roboto", size=18, weight="bold")
        self.error_frame = customtkinter.CTkFrame(self.parent, border_width=3, border_color='red')

        self.error = customtkinter.CTkLabel(self.error_frame,
                                       text="", 
                                       text_color='red', 
                                       font=self.font_label)

    def show(self, row, col, message, col_span=None):
        """
        Display an error message

        Arguments:
            row (int): The row number that the message should appear on
            col (int): The column number that the message should appear on
            message (string): The message that should be displayed
            col_span (int): The number of columns the frame should span
        """
        
        self.error.configure(text=message)
        
        self.error_frame.grid(row=row, column=col, pady=20, columnspan=col_span)
        self.error.grid(row=0, column=0, padx=20, pady=10)

    def hide(self):
        """
        Hides the error message
        """
        self.error_frame.grid_forget()
        self.error.grid_forget()
