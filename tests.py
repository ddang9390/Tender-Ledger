# Author - Daniel Dang
# Filename - tests.py
# Purpose - Contains test cases for ensuring that the code in the project works properly

import unittest
from src.tender_ledger.Backend.database import *
from src.tender_ledger.Backend.categories import *
from src.tender_ledger.Backend.expenses import *
from src.tender_ledger.Backend.payment_methods import *
from src.tender_ledger.Backend.users import *

TEST_DB_NAME = "test_tender_ledger.db"
TEST_DB_PATH = DB_DIR + "/" + TEST_DB_NAME

#TODO - break apart into multiple test files
class Tests(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.db = DatabaseManager(testing=True)
        self.user_id = -99
        
    # For testing user functionality
    def test_adding_users(self):
        """
        Tests if the user can be added properly
        """
        self.db.clear_tables()
        username = "username"
        password = "123456"

        try:
            result = add_user(username, password, self.db)
            delete_user(username, self.db)

            self.assertTrue(result)
        except Exception as e:
            self.fail("Unable to add user")

    def test_unable_to_add_duplicate_user(self):
        """
        Tests if unable to add users with duplicate usernames
        """
        self.db.clear_tables()
        username = "duplicate"
        password = "123456"

        try:
            result = add_user(username, password, self.db)
            result = add_user(username, password, self.db)

            self.assertFalse(result)
        except Exception as e:
            self.fail("Unable to add user")

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
        self.db.clear_tables()
        username = "delete_me"
        password = "123456"

        try:
            result = add_user(username, password, self.db)
            result = delete_user(username, self.db)

            self.assertTrue(result)
        except Exception as e:
            print(e)
            self.fail("Unable to delete user")
        


    # For testing category functionality
    def test_adding_categories(self):
        """
        Tests if the category can be added properly
        """
        self.db.clear_tables()
        try:
            result = add_category(self.user_id, "testing", self.db)
            self.assertTrue(result)
        except Exception as e:
            print(e)
            self.fail("Unable to add category")


    def test_unable_to_add_duplicate_category(self):
        """
        Tests if unable to add category with duplicate names
        """
        self.db.clear_tables()
        try:
            result = add_category(self.user_id, "testing", self.db)
            result = add_category(self.user_id, "testing", self.db)
            self.assertFalse(result)
        except Exception as e:
            print(e)
            self.fail("Unable to add category")

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

    def test_get_default_categories(self):
        """
        Tests if able to get default categories for user
        """  
        self.db.clear_tables()
        try:
            result = get_categories_for_user(self.user_id, self.db)
            self.assertEqual(len(result.keys()), 9)
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return {}
        
    def test_get_categories_for_user(self):
        """
        Tests if able to get categories for user
        """  
        self.db.clear_tables()
        try:
            add_category(self.user_id, "testing", self.db)
            result = get_categories_for_user(self.user_id, self.db)
            self.assertEqual(len(result.keys()), 10)
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return {}
        
    def test_not_getting_categories_from_other_users(self):
        """
        Tests if unable to get categories from other users
        """  
        self.db.clear_tables()
        try:
            add_category(self.user_id, "testing", self.db)
            result = get_categories_for_user(-1, self.db)
            self.assertEqual(len(result.keys()), 9)
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return {}


    # For testing payment method functionality
    def test_adding_payment_method(self):
        """
        Tests if the payment method can be added properly
        """
        """
        Tests if the category can be added properly
        """
        self.db.clear_tables()
        try:
            result = add_payment_method(self.user_id, "testing", self.db)
            self.assertTrue(result)
        except Exception as e:
            print(e)
            self.fail("Unable to add payment method")

    def test_unable_to_add_duplicate_payment_method(self):
        """
        Tests if unable to add payment method with duplicate names
        """
        self.db.clear_tables()
        try:
            result = add_payment_method(self.user_id, "testing", self.db)
            result = add_payment_method(self.user_id, "testing", self.db)
            self.assertFalse(result)
        except Exception as e:
            print(e)
            self.fail("Unable to add payment method")

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

    def test_get_default_payment_methods(self):
        """
        Tests if able to get default payment methods for user
        """  
        self.db.clear_tables()
        try:
            result = get_payment_methods_for_user(self.user_id, self.db)
            self.assertEqual(len(result.keys()), 2)
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return {}
        
    def test_get_payment_methods_for_user(self):
        """
        Tests if able to get payment methods for user
        """  
        self.db.clear_tables()
        try:
            add_payment_method(self.user_id, "testing", self.db)
            result = get_payment_methods_for_user(self.user_id, self.db)
            self.assertEqual(len(result.keys()), 3)
        except sqlite3.Error as e:
            print(f"Error fetching payment methods: {e}")
            return {}
        
    def test_not_getting_payment_methods_from_other_users(self):
        """
        Tests if unable to get payment methods from other users
        """  
        self.db.clear_tables()
        try:
            add_payment_method(self.user_id, "testing", self.db)
            result = get_payment_methods_for_user(-1, self.db)
            self.assertEqual(len(result.keys()), 2)
        except sqlite3.Error as e:
            print(f"Error fetching payment methods: {e}")
            return {}


    # For testing expenses functionality
    def test_adding_expense(self):
        """
        Tests if the expense can be added properly
        """
        con = sqlite3.connect(TEST_DB_PATH)
        cur = con.cursor()
        self.db.clear_tables()

        # Parameters for test expense
        user_id = None
        amount = 123
        date_of_purchase = datetime.now()
        payment_method_id = 1
        category_id = 1
        location = "testing"

        try:
            result = add_expense(user_id,amount, date_of_purchase, payment_method_id, category_id, location, self.db)
            con.close()

            self.assertTrue(result)
        except Exception as e:
            print(e)
            self.fail("Unable to delete expense")

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