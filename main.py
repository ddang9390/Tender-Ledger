# Author - Daniel Dang
# Filename - main.py
# Purpose - To execute the main workflow of the project

from src.tender_ledger.Backend.database import set_up_database
from src.tender_ledger.GUI.main_ui import App

def main():
    set_up_database()

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()