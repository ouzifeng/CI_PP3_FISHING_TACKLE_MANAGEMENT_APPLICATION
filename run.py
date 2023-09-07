import gspread
from google.oauth2.service_account import Credentials
import json
import smtplib
from email.mime.text import MIMEText
from prettytable import PrettyTable
import datetime
import re

# Load credentials from creds.json
with open('creds.json', 'r') as file:
    creds = json.load(file)
    smtp_creds = creds['aws_smtp']
    
smtp_server = smtp_creds['server']
smtp_port = smtp_creds['port']
smtp_username = smtp_creds['username']
smtp_password = smtp_creds['password']

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fishing_tackle')

products = SHEET.worksheet('products')

def send_email(recipient_email, subject, out_of_stock_items):
    """Send email using AWS SMTP credentials."""
    
    # Start building the HTML content for the email
    html_content = """
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2>Out of Stock Products</h2>
        <table>
            <tr>
                <th>SKU</th>
                <th>Product Name</th>
                <th>Cost Price</th>
                <th>RRP</th>
                <th>Stock</th>
            </tr>
    """
    
    for item in out_of_stock_items:
        sku = item.get('SKU', '-')
        product_name = item.get('Product Name', '-')
        cost_price = item.get('Cost Price', '-')
        rrp = item.get('RRP', '-')
        stock = item.get('Stock', '-')
        html_content += f"<tr><td>{sku}</td><td>{product_name}</td><td>{cost_price}</td><td>{rrp}</td><td>{stock}</td></tr>"

    # Close the HTML tags
    html_content += """
        </table>
    </body>
    </html>
    """

    msg = MIMEText(html_content, 'html')
    msg['Subject'] = subject
    msg['From'] = 'orders@tackletarts.uk'  # Your verified sending email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as smtp_connection:
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(msg['From'], [msg['To']], msg.as_string())

def check_out_of_stock():
    """Prints out products that are out of stock."""
    records = products.get_all_records()
    out_of_stock_items = [record for record in records if record and record.get('Stock', 1) <= 0]
    
    if not out_of_stock_items:
        print("All products are in stock!")
        return

    # Create a table
    table = PrettyTable()
    
    # Set the headers for the table
    table.field_names = ["SKU", "Product Name", "Cost Price", "RRP", "Stock"]
    
    # Add rows to the table
    for item in out_of_stock_items:
        sku = item.get('SKU', '-')
        product_name = item.get('Product Name', '-')
        cost_price = item.get('Cost Price', '-')
        rrp = item.get('RRP', '-')
        stock = item.get('Stock', '-')
        table.add_row([sku, product_name, cost_price, rrp, stock])
    
    # Print the table
    print(table)

    print("\nWould you like to:")
    print("1. Send an email with these products for you to order")
    print("2. Back to main menu")
    choice = input("Select an option: ")

    if choice == '1':
        recipient_email = input("Enter the email address to send to: ")
        send_email(recipient_email, "Out of Stock Products", out_of_stock_items)

        print("Email sent successfully!")
    elif choice == '2':
        return
    else:
        print("Invalid choice!")
        
def manage_products():
    while True:
        print("\nManage Products:")
        print("1. Update product details")
        print("2. Delete a product")
        print("3. Go back to main menu")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            update_product_details()
        elif choice == '2':
            delete_product()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")
            
def get_integer_input(prompt_message):
    """Prompt the user for a float input. Retry until a valid float is provided."""
    while True:
        value = input(prompt_message)
        try:
            return float(value)
        except ValueError:
            print("Invalid input! Please enter a number.")            
        
def update_product_details():
    sku = input("Enter SKU of the product you want to update: ")

    # Fetch product details using SKU
    cell = products.find(sku)
    
    if cell is None:
        print("Product with SKU", sku, "not found.")
        choice = input("Would you like to create a new product with this SKU? (yes/no): ")
        if choice.lower() == 'yes':
            create_product()
        return
    else:
        row_num = cell.row
        product_row = products.row_values(row_num)

    while True:
        # Display current product details
        print("\nCurrent Product Details:")
        print("SKU:", product_row[0])
        print("1. Product Name:", product_row[1])
        print("2. Cost Price:", product_row[2])
        print("3. RRP:", product_row[3])
        print("4. Stock:", product_row[4])
        print("5. Exit to previous menu")
        print("\nWhich detail would you like to update? (Enter 1 for Product Name, 2 for Cost Price etc, or press Enter to skip):")
        
        choice = input()
        if choice == '1':
            new_value = input("Enter new Product Name: ")
            products.update_cell(row_num, 2, new_value)
        elif choice == '2':
            new_value = get_integer_input("Enter new Cost Price: ")
            products.update_cell(row_num, 3, new_value)
        elif choice == '3':
            new_value = get_integer_input("Enter new RRP: ")
            products.update_cell(row_num, 4, new_value)
        elif choice == '4':
            new_value = get_integer_input("Enter new Stock: ")
            products.update_cell(row_num, 5, new_value)
        elif choice == '5' or choice == '':
            print("Exiting to previous menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            
        # Refresh the product_row after the update so that the latest details are displayed in the next loop iteration
        product_row = products.row_values(row_num)

    print("\nProduct details updated successfully!")
    
def delete_product():
    sku = input("Enter SKU of the product you want to delete: ")

    # Fetch product details using SKU
    cell = products.find(sku)
    
    if cell is None:
        print("\nProduct with SKU", sku, "not found. Please choose another option")
        return
    else:
        row_num = cell.row
        product_row = products.row_values(row_num)
    
    # Display the product details to the user for confirmation
    print("\nProduct Details:")
    print("SKU:", product_row[0])
    print("Product Name:", product_row[1])
    print("Cost Price:", product_row[2])
    print("RRP:", product_row[3])
    print("Stock:", product_row[4])
    
    choice = input("\nAre you sure you want to delete this product? (yes/no): ")

    if choice.lower() == 'yes':
        double_check = input("This action is irreversible. Confirm deletion? (yes/no): ")
        if double_check.lower() == 'yes':
            products.delete_rows(row_num, row_num)
            print("Product deleted successfully!")
        else:
            print("Product deletion canceled.")
    else:
        print("Product deletion canceled.")

def is_valid_email(email):
    """
    Validate the email based on the following:
    - Contains one '@' symbol.
    - Has a domain name after the '@' symbol.
    - Ends with a domain extension like .com, .org, etc.
    """
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """
    Validate the password based on the following:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - No spaces at the beginning or end
    """
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*]", password):
        return False
    if password.strip() != password:
        return False
    return True

def login(email, password):
    users_sheet = SHEET.worksheet('user')
    user_data = users_sheet.get_all_records()

    for user in user_data:
        if user['User'] == email and user['Password'] == password:
            print(f"\nWelcome {email}! You are now logged in.")
            print("Welcome to the fishing tackle management system. You will find options to manage your shop inventory below.")
            return True
    print("\nInvalid email or password.")
    return False

def signup():
    users_sheet = SHEET.worksheet('user')

    email = input("Enter your email: ")

    if not is_valid_email(email):
        print("Invalid email! Please adhere to the requirements.")
        print("- Contains one '@' symbol.")
        print("- Has a domain name after the '@' symbol.")
        print("- Ends with a domain extension like .com, .org, etc.\n")
        return
    
    while True:
        print("\nPassword requirements:")
        print("- At least 8 characters")
        print("- At least one uppercase letter")
        print("- At least one lowercase letter")
        print("- At least one digit")
        print("- At least one special character (e.g., !, @, #, $, etc.)")
        print("- No spaces at the beginning or end")
        password = input("\nEnter a password: ")

        if not is_valid_password(password):
            print("Invalid password! Please adhere to the requirements.")
            continue

        confirm_password = input("Re-enter password to confirm: ")

        if password != confirm_password:
            print("\nPasswords do not match! Please try again.")
            continue
        else:
            break

    user_data = users_sheet.col_values(1)  # Get all emails

    if email in user_data:
        print("Email already exists! Please try another one or log in.")
        return

    # Append the new user data
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_sheet.append_row([email, password, current_time])
    print(f"\nUser with email {email} successfully signed up!")

    # Log the user in automatically
    return login(email, password)

def logged_in_menu():
    while True:
        print("\nWhat would you like to do next?")
        print("1. Manage Inventory")
        print("2. View Sales Data")
        print("3. Log out")
        
        choice = input("Select an option: ")

        if choice == '1':
            # Call a function to manage inventory
            pass
        elif choice == '2':
            # Call a function to view sales data
            pass
        elif choice == '3':
            print("Logged out successfully!")
            break
        else:
            print("Invalid choice!")


def main():
    logged_in = False
    while not logged_in:
        print("\nWhat do you want to do?")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            logged_in = login(email, password)
        elif choice == '2':
            logged_in = signup()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

    if logged_in:
        logged_in_menu()

def user_actions():
    """Function to prompt logged in user for what they want to do."""
    while True:
        print("\nWhat do you want to do?")
        print("1. Show me all out of stock products")
        print("2. Manage products")
        print("3. Create products")
        print("4. Logout")
        
        choice = input("Select an option: ")

        if choice == '1':
            check_out_of_stock()
        elif choice == '2':
            manage_products()
        elif choice == '3':
            create_product()
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

# ... [rest of your code]

if __name__ == "__main__":
    main()

