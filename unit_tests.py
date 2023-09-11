import unittest
from utilities import (
    is_valid_email, is_valid_password, get_integer_input,
    is_passwords_match, calculate_profit_margin
)
from authentication import login
from unittest.mock import patch
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets authentication
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fishing_tackle')
test_users_sheet = SHEET.worksheet('test_user')
products_sheet = SHEET.worksheet('products')


class TestUtilities(unittest.TestCase):

    def test_valid_email(self):
        self.assertTrue(is_valid_email("example@email.com"))

    def test_invalid_email_no_at_symbol(self):
        self.assertFalse(is_valid_email("exampleemail.com"))

    def test_invalid_email_no_domain(self):
        self.assertFalse(is_valid_email("example@"))

    def test_invalid_email_no_username(self):
        self.assertFalse(is_valid_email("@email.com"))

    def test_empty_email(self):
        self.assertFalse(is_valid_email(""))


class TestPasswordValidation(unittest.TestCase):

    def test_valid_password(self):
        self.assertTrue(is_valid_password("Password1!"))

    def test_invalid_password_short_length(self):
        self.assertFalse(is_valid_password("Pass1!"))

    def test_invalid_password_no_uppercase(self):
        self.assertFalse(is_valid_password("password1!"))

    def test_invalid_password_no_lowercase(self):
        self.assertFalse(is_valid_password("PASSWORD1!"))

    def test_invalid_password_no_digit(self):
        self.assertFalse(is_valid_password("Password!"))

    def test_invalid_password_no_special_character(self):
        self.assertFalse(is_valid_password("Password1"))

    def test_password_with_spaces_at_ends(self):
        self.assertFalse(is_valid_password(" Password1! "))


class TestGetIntegerInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['a', 'b', '1.23'])
    def test_get_integer_input(self, mock_input):
        self.assertEqual(get_integer_input("Enter number: "), 1.23)


class TestPasswordMatch(unittest.TestCase):

    def test_passwords_match(self):
        self.assertTrue(is_passwords_match("password", "password"))

    def test_passwords_do_not_match(self):
        self.assertFalse(is_passwords_match("password", "password123"))


class TestCalculateProfitMargin(unittest.TestCase):

    def test_positive_profit_margin(self):
        self.assertEqual(calculate_profit_margin(50, 100), 0.5)

    def test_zero_profit_margin(self):
        self.assertEqual(calculate_profit_margin(100, 100), 0)

    def test_negative_profit_margin(self):
        self.assertEqual(calculate_profit_margin(150, 100), -0.5)


class TestAuthentication(unittest.TestCase):

    @patch('builtins.input', side_effect=['test@email.com', 'TestPassword1!'])
    def test_valid_login(self, mock_input):
        result = login(sheet=test_users_sheet)
        self.assertTrue(result)


class _TestResult(unittest.TextTestResult):

    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write('PASS ')
        self.stream.write(self.getDescription(test))
        self.stream.write("\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write('FAIL ')
        self.stream.write(self.getDescription(test))
        self.stream.write("\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write('ERROR ')
        self.stream.write(self.getDescription(test))
        self.stream.write("\n")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.stream.write('SKIP ')
        self.stream.write(self.getDescription(test))
        self.stream.write(f" ({reason})\n")


class _TestRunner(unittest.TextTestRunner):
    resultclass = _TestResult


if __name__ == "__main__":
    unittest.main(testRunner=_TestRunner)
