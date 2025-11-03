# Author - Daniel Dang
# Filename - dashboard_page.py
# Purpose - Handles the appearance of the dashboard page

import customtkinter
from ...Backend.expenses import get_expenses_for_user, get_total_spending
from ...Backend.dashboard import generate_pie_charts

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the DashboardPage

        Argumgents:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        # TODO - change user id
        self.user_id = -1
        self.expenses = get_expenses_for_user(self.user_id, self.db)

        # Header
        label = customtkinter.CTkLabel(self, text="Dashboard")
        label.grid(row=0, column=0)

        # Filter Section
        # TODO - make date range filters

        # Summary Row
        self.create_summary_section()

        # Tables
        self.create_chart_section()

    def create_summary_section(self):
        """
        Create summary section showing total spending and category with most spending
        """
        self.summary_frame = customtkinter.CTkFrame(self)

        # Display Total Spending label
        # TODO - integrate start and end dates when search section is complete
        total = get_total_spending(self.user_id, self.db)
        total_spending_label = customtkinter.CTkLabel(self.summary_frame, text=f"Total Spending: ${total:.2f}")
        total_spending_label.grid(row=0, column=0)

        self.summary_frame.grid(row=1, column=0)

    def create_chart_section(self):
        """
        Create chart section for dashboard. Includes pie charts for distribution among
        categories and payment methods.
        """
        # Generate pie charts
        category_pie, payment_method_pie = generate_pie_charts(self.expenses)
        self.chart_frame = customtkinter.CTkFrame(self)

        # Display category pie chart
        category_pie_chart = FigureCanvasTkAgg(figure=category_pie, master=self.chart_frame)
        category_pie_chart.get_tk_widget().grid(row=0, column=0)

        # Display payment method pie chart
        payment_method_pie_chart = FigureCanvasTkAgg(figure=payment_method_pie, master=self.chart_frame)
        payment_method_pie_chart.get_tk_widget().grid(row=0, column=1)

        self.chart_frame.grid(row=2, column=0)


    