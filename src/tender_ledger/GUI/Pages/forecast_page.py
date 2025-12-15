# Author - Daniel Dang
# Filename - forecast_page.py
# Purpose - Handles the appearance of the forecast page

import customtkinter
import platform
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ...Backend.expenses import get_expenses_for_user, get_total_spending
from ...Backend.forecast import forecast

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FORECAST_PERIOD_OPTIONS = {
    "Next 30 Days" : 1,
    "Next 60 Days" : 2,
    "Next 90 Days" : 3
}
HISTORICAL_DATA_OPTIONS = {
    "All Time" : None,
    "Last 3 Months" : 3,
    "Last 6 Months" : 6,
    "Last 12 Months" : 12
}

class ForecastPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller, db):
        """
        Initializes a new instance of the ForecastPage

        Arguments:
            parent (CTkFrame): The container that will be containing this page
            controller (App): The main ui that acts as a controller for deciding what page is visible
            db (DatabaseManager): Instance of database manager being used
        """
        super().__init__(parent)
        self.controller = controller
        self.db = db

        self.start_date = None
        self.end_date = None

        # Have elements in main container expand properly
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Detect OS for custom scrolling
        self.is_linux = platform.system() in ["Linux"]

        
    def refresh_page(self, user_id):
        """
        Updates the page

        Argument:
            user_id (int): The user's id
        """
        self.user_id = user_id
        self.expenses = get_expenses_for_user(self.user_id, self.db, start_date=self.start_date, end_date=self.end_date)

        # Header
        label = customtkinter.CTkLabel(self, text="Spending Forecast", font=self.controller.font_label)
        label.grid(row=0, column=0, sticky="nsew")
        self.create_header_section()

        # Summary Row
        #self.create_summary_section()  

    def create_header_section(self):
        """
        Create header section that will contain dropdowns for forecast period and historical data range
        along with a button for generating a forecast
        """
        self.header_section = customtkinter.CTkFrame(self)

        # Labels for dropdowns
        forecast_period_label = customtkinter.CTkLabel(self.header_section, text="Forecast Period")
        forecast_period_label.grid(row=0, column=0)
        historical_data_label = customtkinter.CTkLabel(self.header_section, text="Forecast Label")
        historical_data_label.grid(row=0, column=1)

        # Dropdowns
        self.forecast_period = customtkinter.CTkOptionMenu(self.header_section, values=list(FORECAST_PERIOD_OPTIONS.keys()))
        self.forecast_period.grid(row=1, column= 0)
        self.historical_data = customtkinter.CTkOptionMenu(self.header_section, values=list(HISTORICAL_DATA_OPTIONS.keys()))
        self.historical_data.grid(row=1, column= 1)

        # Button
        generate_forecast = customtkinter.CTkButton(self.header_section, text="Generate Forecast", command=self.forecast)
        generate_forecast.grid(row=1, column=2)

        self.header_section.grid(row=1, column=0)

    def forecast(self):
        """
        Predict future spending and detect anomalies
        """
        forecast_period = self.forecast_period.get()
        months = HISTORICAL_DATA_OPTIONS[self.historical_data.get()]

        # Get expenses
        current_day = datetime.now() if months else None
        start_date = current_day - relativedelta(months=months) if months else None
        self.expenses = get_expenses_for_user(self.user_id, self.db, start_date=start_date, end_date=current_day)


        forecast(self.expenses)



    