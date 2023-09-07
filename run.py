import gspread
from google.oauth2.service_account import Credentials
import json
import smtplib
from email.mime.text import MIMEText
from prettytable import PrettyTable

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


def main():
    """Main function to prompt user for what they want to do."""
    while True:
        print("\nWhat do you want to do?")
        print("1. Show me all out of stock products")
        print("2. Exit Application")
        
        choice = input("Select an option: ")

        if choice == '1':
            check_out_of_stock()
        elif choice == '2':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
