# Author - Daniel Dang
# Filename - dashboard_page.py
# Purpose - Handles the appearance of the dashboard page

import customtkinter
from ...Backend.expenses import get_expenses_for_user, get_total_spending
from ...Backend.dashboard import generate_pie_charts, generate_line_plot

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

        # Have elements in main container expand properly
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        # TODO - change user id
        self.user_id = user_id
        self.expenses = get_expenses_for_user(self.user_id, self.db)

        # Header
        label = customtkinter.CTkLabel(self, text="Dashboard", font=self.controller.font_label)
        label.grid(row=0, column=0, columnspan=2,sticky="nsew")

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

        if total == None:
            total = 0

        total_spending_label = customtkinter.CTkLabel(self.summary_frame, text=f"Total Spending: ${total:.2f}", font=self.controller.font_label)
        total_spending_label.pack(side="left")

        self.summary_frame.grid(row=1, column=0, columnspan=2,sticky="nsew")

    def create_chart_section(self):
        """
        Create chart section for dashboard. Includes pie charts for distribution among
        categories and payment methods.
        """
        # Generate pie charts
        category_pie, payment_method_pie = generate_pie_charts(self.expenses)
        self.chart_frame = customtkinter.CTkScrollableFrame(self)
        self.chart_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Allow for columns in frame to be able to expand to fit in frame
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(1, weight=1)

        # Handle scrolling with mouse wheel
        self.chart_frame.bind("<Enter>", lambda event: self.bind_mousewheel())
        self.chart_frame.bind("<Leave>", lambda event: self.unbind_mousewheel())

        # Display category pie chart
        category_chart_container = customtkinter.CTkFrame(self.chart_frame)
        category_chart_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        category_pie_chart = FigureCanvasTkAgg(figure=category_pie, master=category_chart_container)
        category_pie_chart.get_tk_widget().pack()
        

        # Display payment method pie chart
        payment_container = customtkinter.CTkFrame(self.chart_frame)
        payment_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        payment_method_pie_chart = FigureCanvasTkAgg(figure=payment_method_pie, master=payment_container)
        payment_method_pie_chart.get_tk_widget().pack()

        # Display line graph
        line_container = customtkinter.CTkFrame(self.chart_frame)
        line_container.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
        
        line_plot = generate_line_plot(self.expenses)
        line_plot_chart = FigureCanvasTkAgg(figure=line_plot, master=line_container)
        line_plot_chart.get_tk_widget().pack()

    
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