# Author - Daniel Dang
# Filename - dashboard_page.py
# Purpose - Handles the appearance of the dashboard page

import customtkinter
import platform
from datetime import datetime
from ...Backend.expenses import get_expenses_for_user, get_total_spending
from ...Backend.dashboard import generate_pie_charts, generate_line_plot, generate_bar_chart
from ..Elements.filter_section import FilterSection

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the DashboardPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        # Have elements in main container expand properly
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Detect OS for custom scrolling
        self.is_linux = platform.system() in ["Linux"]

        self.start_date = None
        self.end_date = None

        # Create Filter Section
        self.filter_frame = customtkinter.CTkFrame(self)
        self.filter_frame.grid(row=1, column=1, columnspan=2)
        self.filter_section = FilterSection(self.filter_frame, self)

        # Initialize date range label
        self.date_range_label = customtkinter.CTkLabel(self)
        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id
        self.expenses = get_expenses_for_user(self.user_id, self.db, start_date=self.start_date, end_date=self.end_date)

        # Header
        label = customtkinter.CTkLabel(self, text="Dashboard", font=self.controller.font_label)
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Date Range Label
        self.create_date_range_label()

        # Summary Row
        self.create_summary_section()

        # Tables
        self.create_chart_section()

    def create_date_range_label(self):
        """
        Create the date range label showing the earliest and latest expense dates
        """
        # Reset date range label
        if self.date_range_label is not None:
            self.date_range_label.destroy()
            self.date_range_label = None

        date_range_text = "No expenses"
        
        if self.expenses:
            # Get all dates from expenses
            dates = [datetime.strptime(expense[1], "%Y-%m-%d").date() for expense in self.expenses]
            
            if dates:
                earliest_date = min(dates)
                latest_date = max(dates)
                
                # Format dates
                earliest_str = earliest_date.strftime("%b %d, %Y")
                latest_str = latest_date.strftime("%b %d, %Y")
                
                date_range_text = f"Date Range:\n{earliest_str} - {latest_str}"
        
        # Create date range label
        self.date_range_label = customtkinter.CTkLabel(
            self, 
            text=date_range_text,
            font=("Roboto", 20, "bold"),
            justify="left"
        )
        self.date_range_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)


    def create_summary_section(self):
        """
        Create summary section showing total spending and category with most spending
        """
        self.summary_frame = customtkinter.CTkFrame(self)

        # Display Total Spending label
        total = get_total_spending(self.user_id, self.db, self.start_date, self.end_date)

        total_spending_label = customtkinter.CTkLabel(self.summary_frame, text=f"Total Spending: ${total:.2f}", font=self.controller.font_label)
        total_spending_label.grid(row=0, column=0)

        # Display Total Number of Purchases
        total_purchases = len(self.expenses)
        total_purchases_label = customtkinter.CTkLabel(self.summary_frame, text=f"Total Purchases: {total_purchases}", font=self.controller.font_label)
        total_purchases_label.grid(row=0, column=1, padx=20)

        self.summary_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

    def filter_page(self):
        """
        Filters the dashboard page
        """
        if self.filter_section.start_date.get() == "":
            self.start_date = None
        else:
            self.start_date = self.filter_section.start_date.get_date()

        if self.filter_section.end_date.get() == "":
            self.end_date = None
        else:
            self.end_date = self.filter_section.end_date.get_date()

        self.refresh_page(self.user_id)

    def create_chart_section(self):
        """
        Create chart section for dashboard. Includes pie charts for distribution among
        categories and payment methods.
        """
        # Generate pie charts
        category_pie, payment_method_pie = generate_pie_charts(self.expenses)
        self.chart_frame = customtkinter.CTkScrollableFrame(self)
        self.chart_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # Allow for columns in frame to be able to expand to fit in frame
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(1, weight=1)

        # Handle scrolling with mouse wheel
        if self.is_linux:
            self.chart_frame.bind("<Enter>", lambda event: self.bind_mousewheel())
            self.chart_frame.bind("<Leave>", lambda event: self.unbind_mousewheel())

        # Display line graph
        line_container = customtkinter.CTkFrame(self.chart_frame)
        line_container.grid(row=0, column=0, pady=20, sticky="nsew")
        
        line_plot = generate_line_plot(self.expenses)
        line_plot_chart = FigureCanvasTkAgg(figure=line_plot, master=line_container)
        line_plot_chart.get_tk_widget().pack()

        # Display category pie chart
        category_chart_container = customtkinter.CTkFrame(self.chart_frame)
        category_chart_container.grid(row=0, column=1, padx=10)

        category_pie_chart = FigureCanvasTkAgg(figure=category_pie, master=category_chart_container)
        category_pie_chart.get_tk_widget().pack()
        

        # Display bar chart
        bar_container = customtkinter.CTkFrame(self.chart_frame)
        bar_container.grid(row=1, column=0, pady=20)

        bar_chart = generate_bar_chart(self.expenses)
        bar_chart_fig = FigureCanvasTkAgg(figure=bar_chart, master=bar_container)
        bar_chart_fig.get_tk_widget().pack()


        # Display payment method pie chart
        payment_container = customtkinter.CTkFrame(self.chart_frame)
        payment_container.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")

        payment_method_pie_chart = FigureCanvasTkAgg(figure=payment_method_pie, master=payment_container)
        payment_method_pie_chart.get_tk_widget().pack()

        

    
    def bind_mousewheel(self):
        """
        Bind mouse wheel to scrolling when mouse enters the scrollable frame
        """
        self.chart_frame.bind_all("<MouseWheel>", self.on_mousewheel)

        # For Linux
        self.chart_frame.bind_all("<Button-4>", self.on_mousewheel)
        self.chart_frame.bind_all("<Button-5>", self.on_mousewheel)

    def unbind_mousewheel(self):
        """
        Unbind mouse wheel when mouse leaves the scrollable frame
        """
        self.chart_frame.unbind_all("<MouseWheel>")

        # For Linux
        self.chart_frame.unbind_all("<Button-4>")
        self.chart_frame.unbind_all("<Button-5>")

    def on_mousewheel(self, event):
        """
        Handle mouse wheel scrolling
        """
        # Scrolling up
        if event.num == 4 or event.delta > 0:
            self.chart_frame._parent_canvas.yview_scroll(-1, "units")
            
        # Scrolling down
        elif event.num == 5 or event.delta < 0:
            self.chart_frame._parent_canvas.yview_scroll(1, "units")

    