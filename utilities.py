import re


def is_valid_email(email):
    """Email structure validation"""
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)


def is_valid_password(password):
    """Password requirements validation"""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    special_characters = [
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '='
    ]
    if not any(char in special_characters for char in password):
        return False
    if password[0] == ' ' or password[-1] == ' ':
        return False
    return True


def get_integer_input(prompt_message):
    """Checks to see whether an int was used for prices"""
    while True:
        value = input(prompt_message)
        try:
            return float(value)
        except ValueError:
            print("Invalid input! Please enter a number.")


def calculate_profit_margin(cost_price, selling_price):
    """Calculates profit margin as a %"""
    try:
        return (selling_price - cost_price) / selling_price
    except ZeroDivisionError:
        return 0


def is_passwords_match(password1, password2):
    """Checks both passwords match on login"""
    return password1 == password2
