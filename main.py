# Author - Daniel Dang
# Filename - main.py
# Purpose - To execute the main workflow of the project

from src.tender_ledger.Backend.database import set_up_database

def main():
    set_up_database()

if __name__ == "__main__":
    main()