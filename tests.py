# Author - Daniel Dang
# Filename - tests.py
# Purpose - Contains test cases for ensuring that the code in the project works properly

import unittest
from src.tender_ledger.Backend.database import *
from src.tender_ledger.Backend.categories import *
from src.tender_ledger.Backend.expenses import *
from src.tender_ledger.Backend.payment_methods import *
from src.tender_ledger.Backend.users import *

#TODO - break apart into multiple test files
class Tests(unittest.TestCase):
    def test_setup_database(self):
        """
        Tests if the database can be setup properly
        """
        try:
            set_up_database(testing=True)
        except Exception as e:
            print(e)
            self.fail("Unable to setup testing database")
        
    # For testing user functionality
    def test_adding_users(self):
        """
        Tests if the user can be added properly
        """
        pass

    def test_unable_to_add_duplicate_user(self):
        """
        Tests if unable to add users with duplicate usernames
        """
        pass

    def test_password_requirements(self):
        """
        Tests if password requirements are working properly
        """
        pass

    def test_update_user(self):
        """
        Tests if able to update users
        """
        pass

    def test_delete_user(self):
        """
        Tests if able to delete users
        """
        pass


    # For testing category functionality
    def test_adding_categories(self):
        """
        Tests if the category can be added properly
        """
        pass

    def test_unable_to_add_duplicate_category(self):
        """
        Tests if unable to add category with duplicate names
        """
        pass

    def test_update_category(self):
        """
        Tests if able to update categories
        """
        pass

    def test_delete_category(self):
        """
        Tests if able to delete category
        """
        pass



    # For testing payment method functionality
    def test_adding_payment_method(self):
        """
        Tests if the payment method can be added properly
        """
        pass

    def test_unable_to_add_duplicate_payment_method(self):
        """
        Tests if unable to add payment method with duplicate names
        """
        pass

    def test_update_payment_method(self):
        """
        Tests if able to update payment method
        """
        pass

    def test_delete_payment_method(self):
        """
        Tests if able to delete payment method
        """
        pass


    # For testing expenses functionality
    def test_adding_expense(self):
        """
        Tests if the expense can be added properly
        """
        pass

    def test_update_expense(self):
        """
        Tests if able to update expense
        """
        pass

    def test_delete_expense(self):
        """
        Tests if able to delete expense
        """
        pass

if __name__ == "__main__":
    unittest.main()