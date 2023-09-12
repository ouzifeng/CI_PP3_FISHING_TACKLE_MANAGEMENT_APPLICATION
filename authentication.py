import datetime
import re

from google.oauth2.service_account import Credentials
import gspread

from utilities import is_valid_email, is_valid_password

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fishing_tackle')
users_sheet = SHEET.worksheet('user')
test_users_sheet = SHEET.worksheet('test_user')


def login(sheet=users_sheet):
    """Allows the user to log in."""
    while True:
        try:
            email = input("Enter your email (or press Enter to go back): ")

            if not email:
                return False

            if not is_valid_email(email):
                raise ValueError("\nInvalid email format!")

            user_data = sheet.get_all_records()
            email_records = [user['User'] for user in user_data]

            if email not in email_records:
                raise ValueError("\nEmail not found in our database.")

            password = input("Enter your password "
                             "(or press Enter to go back): ")

            for user in user_data:
                if (user['User'] == email and
                        user['Password'] == password):
                    last_login = user['Last Login']
                    print(f"\nWelcome {email}! You are now logged in.")
                    if last_login:
                        print(f"Your last login was on {last_login}.")
                    update_last_login(email)
                    return True

            raise ValueError("\nInvalid password!")

        except ValueError as e:
            print(e)
            continue


def signup(sheet=users_sheet):
    """Allows a user to sign up."""
    while True:
        try:
            email = input("Enter your email: ")
            if not is_valid_email(email):
                raise ValueError("Invalid email! "
                                 "Please adhere to the requirements.")
            user_data = sheet.col_values(1)
            if email in user_data:
                raise ValueError("Email already exists! "
                                 "Please try another one or log in.")
            break
        except ValueError as e:
            print(e)
            continue

    while True:
        try:
            print("\nPassword requirements:")
            print("- At least 8 characters")
            print("- At least one uppercase letter")
            print("- At least one lowercase letter")
            print("- At least one digit")
            print("- At least one special character "
                  "(e.g., !, @, #, $, etc.)")
            print("- No spaces at the beginning or end")

            password = input("\nEnter a password: ")

            if not is_valid_password(password):
                raise ValueError("Invalid password! "
                                 "Please adhere to the requirements.")

            confirm_password = input("Re-enter password to confirm: ")
            if password != confirm_password:
                raise ValueError("\nPasswords do not match! Please try again.")
            break
        except ValueError as e:
            print(e)
            continue

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([email, password, current_time])
    print(f"\nUser with email {email} successfully signed up!")
    return True


def update_last_login(email, sheet=users_sheet):
    """Updates and saves the last time the user signed in"""
    cell = sheet.find(email)
    row_num = cell.row
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.update_cell(row_num, 3, current_time)
