# Author - Daniel Dang
# Filename - main.py
# Purpose - To execute the main workflow of the project

from src.tender_ledger.GUI.main_ui import App
from src.tender_ledger.Backend.database import DatabaseManager

def main():
    db = DatabaseManager()

    app = App(db)
    app.mainloop()

if __name__ == "__main__":
    main()