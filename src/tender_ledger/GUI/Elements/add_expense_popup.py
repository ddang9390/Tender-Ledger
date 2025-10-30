# Author - Daniel Dang
# Filename - add_expense_popup.py
# Purpose - Handles the appearance and fucntion of the Add Expense popup

import customtkinter
from tkcalendar import DateEntry


# Defining constants
ADD_TITLE = "Add Expense"
UPDATE_TITLE = "Edit Expense"

class AddExpensePopup(customtkinter.CTkToplevel):
    def __init__(self, parent, controller, editing=False):
        """
        Initializes a new instance of the ProfilePage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        if editing:
            self.title(UPDATE_TITLE)
        else:
            self.title(ADD_TITLE)
            

        self.setup_inputs()
        self.setup_buttons(editing)

        

    def setup_inputs(self):
        """
        Set up the input fields for adding/updating expenses
        """
        # Setting up overall display of input frame
        input_frame = customtkinter.CTkFrame(self)
        input_frame.grid(row=0, column=0, sticky="nsew")

        # Setting up date field
        date_label = customtkinter.CTkLabel(input_frame, text="Date:")
        date_label.grid(row=0, column=0)
        self.date = DateEntry(input_frame, selectmode='day')
        self.date.grid(row=0, column=1)

        # Setting up amount field
        amount_label = customtkinter.CTkLabel(input_frame, text="Amount:")
        amount_label.grid(row=1, column=0)
        self.amount = customtkinter.CTkEntry(input_frame)
        self.amount.grid(row=1, column=1)

        # Setting up category field
        # self.category = 

        # Setting up Method of Purchase field
        # self.method_of_purchase = 

        # Setting up Location field
        # self.location = 

    def setup_buttons(self, editing):
        """
        Set up the buttons for the expense popup

        Argument:
            editing (bool): True if we are updating an expense
                            Else we are adding an expense
        """
        # Setting up overall display of button frame
        button_frame = customtkinter.CTkFrame(self)
        button_frame.grid(row=1, column=0)

        add_button = customtkinter.CTkButton(button_frame, text="Add", command=self.add_expense)
        add_button.pack(side="right")
        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left")


    def add_expense(self):
        """
        Adds the expense when all required fields are filled out
        """
        print(self.date.get_date())