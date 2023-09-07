import gspread
from google.oauth2.service_account import Credentials
import json
import smtplib

# Load credentials from creds.json
with open('creds.json', 'r') as file:
    creds = json.load(file)
    smtp_creds = creds['aws_smtp']

# Connect to the SMTP server using the loaded credentials
smtp_server = smtp_creds['server']
smtp_port = smtp_creds['port']
smtp_username = smtp_creds['username']
smtp_password = smtp_creds['password']

smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()
smtp_connection.login(smtp_username, smtp_password)

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

def check_out_of_stock():
    """Prints out products that are out of stock."""
    records = products.get_all_records()
    out_of_stock_items = [record for record in records if record['Stock'] <= 0]
    
    for item in out_of_stock_items:
        print(item['Product Name'], "-", item['Description'])
    