# Author - Daniel Dang
# Filename - notification.py
# Purpose - Handles the appearance and behavior of the notification

import customtkinter

class Notification(customtkinter.CTkFrame):
    def __init__(self, parent, message):
        """
        Creates a notification popup
        """
        super().__init__(parent, border_width=2, border_color="white")

        # Place the notification
        self.place(relx=0.5, rely=0.02, anchor="n") 

        # Notification's label
        self.label = customtkinter.CTkLabel(
            self,
            text=message,
            text_color="white",
            font=("Roboto", 14, "bold"),
            width=250
        )
        self.label.pack(padx=20, pady=10)
        
        # Add a close button
        self.close_btn = customtkinter.CTkButton(
            self, 
            text="×", 
            width=20, 
            height=20,
            fg_color="transparent", 
            text_color="white",
            font=("Arial", 16, "bold"),
            command=self.destroy
        )
        self.close_btn.place(relx=0.95, rely=0.1, anchor="ne")

        # Keep notification in the front and destroy it after 3s
        self.lift()
        self.after(3000, self.destroy)