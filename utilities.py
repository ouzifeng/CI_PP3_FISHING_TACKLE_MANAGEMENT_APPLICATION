import re

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    if not any(char in special_characters for char in password):
        return False
    if password[0] == ' ' or password[-1] == ' ':
        return False
    return True

def get_integer_input(prompt_message):
    while True:
        value = input(prompt_message)
        try:
            return float(value)
        except ValueError:
            print("Invalid input! Please enter a number.")
