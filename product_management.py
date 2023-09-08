from utilities import get_integer_input
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
products = SHEET.worksheet('products')

def update_product_details():
    sku = input("Enter SKU of the product you want to update: ")
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
        product_row = products.row_values(row_num)
    print("\nProduct details updated successfully!")
    
def delete_product():
    sku = input("Enter SKU of the product you want to delete: ")
    cell = products.find(sku)
    if cell is None:
        print("\nProduct with SKU", sku, "not found. Please choose another option")
        return
    else:
        row_num = cell.row
        product_row = products.row_values(row_num)
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
